import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Production configuration - In a real app, these are fetched from your .env file
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password" 

def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Establishes a secure connection with the SMTP server to send
    real background email notifications to users or recruiters.
    """
    try:
        # Create a container message that can hold text and attachments
        msg = MIMEMultipart()
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_email
        msg["Subject"] = subject
        
        # Attach the raw text body to the email container as plain text
        msg.attach(MIMEText(body, "plain"))
        
        # Initialize the SMTP client and establish a connection to the network provider
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        # Put the SMTP connection into TLS (Transport Layer Security) mode for encryption
        server.starttls()
        
        # Authenticate against the server using the application credentials
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Transmit the message payload securely across the network
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        
        # Gracefully terminate the SMTP session
        server.quit()
        return True
        
    except Exception as e:
        # Production fail-safe logging
        print(f"Failed to send email securely: {str(e)}")
        return False