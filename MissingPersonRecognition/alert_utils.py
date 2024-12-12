import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Email configuration from environment variables
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = os.getenv("kush1707kushal@gmail.com")
EMAIL_PASSWORD = os.getenv("Kush1707")

# Send alert email
def send_email_alert(recipient_email, name, metadata):
    try:
        # Email content
        subject = f"Missing Person Identified: {name}"
        body = f"""
        A missing person has been identified.
        Name: {name}
        Metadata: {metadata}
        Please take the necessary action.
        """

        # Create email message
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"Alert email sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage for testing
if __name__ == "__main__":
    send_email_alert("ysarjun123@gmail.com", "John Doe", {"age": 30, "last_seen": "NYC"})
