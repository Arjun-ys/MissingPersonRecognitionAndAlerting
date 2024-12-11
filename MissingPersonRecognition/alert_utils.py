import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Email configuration (replace these with environment variables)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = os.getenv("EMAIL")  # Environment variable for email
PASSWORD = os.getenv("EMAIL_PASSWORD")  # Environment variable for email password

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
        
        # OAuth2.0 authentication
        import smtplib
        import base64
        import json
        import requests
        
        def get_oauth_token():
            client_id = os.getenv("GMAIL_CLIENT_ID")
            client_secret = os.getenv("GMAIL_CLIENT_SECRET")
            refresh_token = os.getenv("GMAIL_REFRESH_TOKEN")
            
            token_url = "https://accounts.google.com/o/oauth2/token"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            }
            
            response = requests.post(token_url, headers=headers, data=data)
            tokens = response.json()
            return tokens["access_token"]
        
        oauth_token = get_oauth_token()
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp.starttls()
        smtp.login(EMAIL, oauth_token)
        smtp.send_message(msg)
        smtp.quit()
        
        print(f"Alert email sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
