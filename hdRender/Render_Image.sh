#!/bin/bash

email="$1"
image_text="$2"  # This is the image_text passed as the second argument

# Extract the username from the email address
username=$(echo "$email" | cut -d '@' -f 1)
current_datetime=$(date +"_%Y/%d-%m/%H-%M_")

script_path="/hdRender/Render_Image.py"
output_path="/hdRender/Assets/Render_Images/${username}${current_datetime}Render_Image.PNG"

# Run Blender to render the image
/blender-4.3.2-linux-x64/blender -b -P "$script_path" -- "$email" "$image_text"  # Pass image_text as an argument
pwd
# Send the rendered image via email
python3 "/hdRender/Send_Image.py" "$email" "$output_path"
	
