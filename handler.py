import runpod
import torch
from diffusers import FluxPipeline
from PIL import Image
import io
from huggingface_hub import login
# Log in using the Hugging Face token if necessary
login(token='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')
# Define the network volume path for serverless
NETWORK_VOLUME_PATH = "/runpod-volume"

# Set environment variables to use the network volume for model caching
os.environ["HF_HOME"] = f"{NETWORK_VOLUME_PATH}/hf-cache"
os.environ["TRANSFORMERS_CACHE"] = f"{NETWORK_VOLUME_PATH}/hf-cache"

# Initialize the FluxPipeline model once when the handler starts
pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16, use_auth_token=True)
pipe.enable_model_cpu_offload()  # Enable CPU offloading to save VRAM (can be removed if enough GPU memory)

# Define the handler function
def handler(event):
    input_data = event['input']
    prompt = input_data.get('prompt', 'A beautiful sunset over the ocean')  # Default prompt if not provided
    


    try:
        # Generate the image based on the provided prompt
        image = pipe(
            prompt,
            height=1024,
            width=1024,
            guidance_scale=3.5,
            num_inference_steps=50,
            max_sequence_length=512,
            generator=torch.Generator("cpu").manual_seed(0)  # Optional: Seed for reproducibility
        ).images[0]  # Get the first image in the response

        # Convert the image to bytes to send as part of the response
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        # Return the image as a base64-encoded string or a direct image blob
        return {
            'statusCode': 200,
            'body': img_byte_arr,
            'headers': {
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': 'attachment; filename="generated_image.png"'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
