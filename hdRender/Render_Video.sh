#!/bin/bash

email=$1
image_text="$2"  # This is the image_text passed as the second argument

# Extract the username from the email address
username=$(echo "$email" | cut -d '@' -f 1)
current_datetime=$(date +"_%Y/%d-%m/%H-%M_")

script_path="Render_Video.py"
output_path="Assets/Render_Videos/${username}${current_datetime}Render_Video.mp4"

# Run Blender to render the image
blender -b -P "$script_path" -- "$email" "$image_text"  # Pass image_text as an argument

# Send the rendered image via email
python3 "Send_Video.py" "$email" "$output_path"
