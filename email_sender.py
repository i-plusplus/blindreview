import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
# Function to send email
def send_email(email, subject, body):
    try:
        sender_email = "masterofmasters22@gmail.com"
        sender_email = "tojomojoteam@gmail.com"
        sender_password = "axqx tfxq wkuf dzbn"  # Be cautious: don't hardcode passwords in real applications
        sender_password = "olxm twmb rdzl rdex" # for tojomojoteam@gmail.com
        recipient_email = email


        # Set up the email server (e.g., Gmail SMTP server)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the email content
        msg = MIMEMultipart()
        msg['From'] = formataddr(('Tojomojo Team', sender_email))
        msg['To'] = recipient_email
        msg['Subject'] = subject
        # Attach the email body
        msg.attach(MIMEText(body, 'html'))

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)

        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")

        # Close the server connection
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
if __name__ == "__main__":
    body = 'test boxy'
    send_email(body)
