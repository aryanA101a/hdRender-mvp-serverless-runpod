import runpod
import requests
import os
from hdRender.rendur import renderImage

def download_glb(glb_url):
    """Downloads the GLB file from the provided S3 URL."""
    try:
        response = requests.get(glb_url)
        response.raise_for_status()
        return response.content  # Return binary data of the file
    except requests.exceptions.RequestException as e:
        print(f"Error downloading GLB: {e}")
        return None

def handler(event):
    input = event['input']
    glb_url = input.get('glbUrl')
    resolution = input.get('resolution')
    email = input.get('email')

    if not glb_url:
        return {'error': 'GLB URL missing'}

    glb_file_data = download_glb(glb_url)
    
    if glb_file_data is None:
        return {'error': 'Failed to download GLB file'}

    result = renderImage(glb_file_data, resolution, email)
    return result

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})