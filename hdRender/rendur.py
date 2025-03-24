import subprocess
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def asli_render(email, file_path, file_data, image_text):
        with open(file_path, 'wb') as f:
            f.write(file_data)
        subprocess.Popen(['bash', '/hdRender/Render_Image.sh', email, str(image_text)])
        send_notification_email(email, 'GLB file received and added to the queue for rendering')

def send_notification_email(email, message):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'viscommercecdn@gmail.com'
    SMTP_PASSWORD = 'valdzjcmddlqarob'
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




def renderImage(glbFileData,res,email):
    print(email)
    temp_file_path = os.path.join('/hdRender/Assets/GLB_Files/', f'{email}.glb')
    asli_render(email,temp_file_path, glbFileData, res)


