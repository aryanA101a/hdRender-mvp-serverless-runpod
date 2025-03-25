import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email_with_image(email, image_path):
    Sender_Email = "viscommercecdn@gmail.com"
    Sender_Password = "vmtjuhjkolsbpdey"
    Receiver_Email = email

    # Compose the email message
    msg = MIMEMultipart()
    msg['From'] = Sender_Email
    msg['To'] = Receiver_Email
    msg['Subject'] = 'Your HD Render is Here!'

    body = """\
Hi,

Your HD render is here, and we can't wait for you to see it! Attached you'll find the image you requested.

HD renders are like a magic wand, turning your creative ideas into high-definition reality. We use high-fidelity, photo-realistic images and PBR (Physically Based Rendering) to capture every nuance and detail of your project, making the decision-making process much easier and more enjoyable. Whether you're visualizing a new space or designing a product, HD renders give you the power to experience your creation before it becomes a reality.

For businesses, this means greater profitability through faster project approvals and enhanced customer experiences.
For end-users like you, HD renders add value by providing a realistic preview of your ideas, helping you make better decisions and ensuring your satisfaction.

We hope you love it as much as we enjoyed creating it for you. If you need anything else, just let us know!

Cheers,
The VisCommerce Team
        """

    msg.attach(MIMEText(body, 'plain'))

    # Attach the rendered image to the email message
    with open(image_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename="rendered_image.png")
        msg.attach(img)

    # Send the email using SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(Sender_Email, Sender_Password)
        server.send_message(msg)

    print("Email Sent")

if __name__ == "__main__":
    email = sys.argv[1]
    image_path = sys.argv[2]
    send_email_with_image(email, image_path)
