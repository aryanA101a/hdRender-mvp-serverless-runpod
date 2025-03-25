import subprocess
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def asli_render(email, file_path, file_data, image_text):
    with open(file_path, 'wb') as f:
        f.write(file_data)
    
    # Send initial notification email
    send_notification_email(email, 'GLB file received and added to the queue for rendering')
    
    # Calculate the output path exactly as Blender will
    username = email.split('@')[0]
    current_datetime = datetime.datetime.now().strftime("_%Y/%d-%m/%H-%M_")
    output_filename = username + current_datetime + 'Render_Image.PNG'
    output_path = '/hdRender/Assets/Render_Images/' + output_filename
    
    print(f"Expected render path: {output_path}")
    
    # Run Blender with wait=True to make it complete before continuing
    blender_cmd = [
        '/blender-4.3.2-linux-x64/blender',
        '-b',  # background mode
        '-P', '/hdRender/Render_Image.py',
        '--',  # separator for script arguments
        email,  # This will be sys.argv[5] in the Python script
        str(image_text)  # This will be sys.argv[6] in the Python script (resolution)
    ]
    
    print(f"Starting Blender rendering process...")
    
    # Stream the output in real-time
    try:
        # Start the process and stream output
        process = subprocess.Popen(
            blender_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Display output in real-time and capture the actual output path
        actual_output_path = None
        for line in process.stdout:
            print(line, end='')  # Print the line without additional newline
            # Look for the line where Blender says it saved the file
            if 'Saved:' in line:
                # Extract the actual path that Blender used
                actual_output_path = line.split('Saved: ')[1].strip().strip("'")
        
        # Wait for the process to complete and get return code
        return_code = process.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, blender_cmd)
        
        print("Blender rendering completed successfully")
        
        # Use the actual output path if it was captured, otherwise use the expected path
        if actual_output_path:
            output_path = actual_output_path
            print(f"Using actual output path from Blender: {output_path}")
        
        # Check if the file exists before trying to send it
        if not os.path.exists(output_path):
            print(f"WARNING: Rendered file not found at {output_path}")
            # Try to find the file in the directory
            render_dir = '/hdRender/Assets/Render_Images/'
            files = [f for f in os.listdir(render_dir) if username in f and f.endswith('Render_Image.PNG')]
            if files:
                # Use the most recent file
                files.sort(key=lambda x: os.path.getmtime(os.path.join(render_dir, x)), reverse=True)
                output_path = os.path.join(render_dir, files[0])
                print(f"Found alternative file: {output_path}")
            else:
                print("No suitable render file found.")
                raise FileNotFoundError(f"Rendered image not found at {output_path}")
        
        # Now send the email with the rendered image
        print(f"Sending email with rendered image from path: {output_path}")
        send_image_cmd = ["python3", "/hdRender/Send_Image.py", email, output_path]
        email_process = subprocess.Popen(
            send_image_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Display email sending output in real-time
        for line in email_process.stdout:
            print(line, end='')
            
        # Wait for email process to complete
        email_return_code = email_process.wait()
        if email_return_code != 0:
            raise subprocess.CalledProcessError(email_return_code, send_image_cmd)
            
        print("Process completed: Rendering and email sending finished")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during processing: {e}")
        send_notification_email(email, 'An error occurred during rendering. Please try again.')
    except FileNotFoundError as e:
        print(f"File error: {e}")
        send_notification_email(email, 'An error occurred finding the rendered image. Please try again.')
    except Exception as e:
        print(f"Unexpected error: {e}")
        send_notification_email(email, 'An unexpected error occurred. Please try again.')
        
def send_notification_email(email, message):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'viscommercecdn@gmail.com'
    SMTP_PASSWORD = 'vmtjuhjkolsbpdey'
    SENDER_EMAIL = 'viscommercecdn@gmail.com'
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = 'GLB Rendering Notification'
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())
        server.quit()
        print("Email notification sent successfully")
    except Exception as e:
        print(f"Error sending email notification: {str(e)}")

def renderImage(glbFileData, res, email):
    print(email)
    temp_file_path = os.path.join('/hdRender/Assets/GLB_Files/', f'{email}.glb')
    asli_render(email, temp_file_path, glbFileData, res)