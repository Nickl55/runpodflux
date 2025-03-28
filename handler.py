import runpod
import json
from transformers import pipeline

# Initialize the Hugging Face image generation pipeline
image_gen_pipeline = pipeline("image-generation", model="black-forest-labs/FLUX.1-dev")

def handler(event):
    # Extract input from the event
    input_data = event.get('input', {})
    prompt = input_data.get('prompt')
    seconds = input_data.get('seconds', 0)  # Optional processing time, if you want to simulate delay

    # Check if a prompt is provided
    if not prompt:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Prompt is required'})
        }

    # Simulate processing time if provided
    time.sleep(seconds)

    try:
        # Generate image using the FLUX.1-dev model
        generated_image = image_gen_pipeline(prompt)
        image_url = generated_image[0]["url"]  # Assuming the model's output contains a URL

        # Return the image URL as the response
        return {
            'statusCode': 200,
            'body': json.dumps({'image_url': image_url})
        }

    except Exception as e:
        # Return an error if something goes wrong
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error generating image: {str(e)}'})
        }

if __name__ == '__main__':
    # Start the RunPod serverless service
    runpod.serverless.start({'handler': handler})
