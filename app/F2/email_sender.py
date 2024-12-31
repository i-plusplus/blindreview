import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email
def send_email(otp, email):
    try:
        sender_email = "masterofmasters22@gmail.com"
        sender_password = "axqx tfxq wkuf dzbn"  # Be cautious: don't hardcode passwords in real applications
        recipient_email = email
        subject = "Test Email " + otp

        # Set up the email server (e.g., Gmail SMTP server)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg['body'] = 'body is nothing'
        # Attach the email body
        msg.attach(MIMEText('body', 'plain'))

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)

        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")

        # Close the server connection
        server.quit()
        return 'Yes'
    except Exception as e:
        print(e)
        return 'No'



# Example usage
if __name__ == "__main__":
    body = 'test boxy'
    send_email(body)
