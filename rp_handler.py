import runpod
import datetime
import time
import os
import json
import base64
from hdRender.rendur import renderImage

def decode_glb(base64_text):
    """Decodes a Base64-encoded GLB file and saves it."""
    try:
        glb_data = base64.b64decode(base64_text)
        
        return glb_data
    except Exception as e:
        print(f"Error decoding GLB: {e}")

def handler(event):
    input = event['input']
    glbBase64 = input.get('glbBase64')
    resolution = input.get('resolution')
    email = input.get('email')

    glbFileData=decode_glb(glbBase64)
    
    result = renderImage(glbFileData,resolution,email)

    return result

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
    
