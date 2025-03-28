import os
import json
from transformers import pipeline

# Initialize the model once to avoid reloading for every request.
# If using a different model, you can adjust this pipeline accordingly.
image_gen_pipeline = pipeline("image-generation", model="black-forest-labs/FLUX.1-dev")

def handler(event, context):
    """
    This function will be triggered by the serverless endpoint.
    It will process the incoming event and generate an image.
    """
    
    # Parse input data from event
    try:
        body = json.loads(event['body'])
        prompt = body.get('prompt', None)
        if not prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Prompt is required'})
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Error parsing the input: {str(e)}'})
        }
    
    # Generate the image using the model
    try:
        generated_image = image_gen_pipeline(prompt)
        
        # Assuming the model returns a list of images in some form
        image_url = generated_image[0]["url"]
        
        # Return the image URL or base64 encoded image data (depending on the model's output)
        return {
            'statusCode': 200,
            'body': json.dumps({'image_url': image_url})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error generating image: {str(e)}'})
        }

