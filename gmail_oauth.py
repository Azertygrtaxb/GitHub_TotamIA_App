import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64

logger = logging.getLogger(__name__)

def get_gmail_sender():
    """Gets a Gmail SMTP sender with password authentication."""
    try:
        logger.info("Initializing Gmail SMTP connection")
        gmail_user = os.environ.get("GMAIL_USER_ADDRESS")
        gmail_password = os.environ.get("GMAIL_PASSWD")

        if not gmail_user or not gmail_password:
            logger.error("Missing Gmail credentials in environment variables")
            return None

        return {
            'user': gmail_user,
            'password': gmail_password
        }
    except Exception as e:
        logger.error(f"Error retrieving Gmail credentials: {e}")
        return None

def create_message_with_attachment(sender, to, subject, html_content, attachment_path=None, attachment_name=None):
    """Create a message for an email with HTML content and optional attachment."""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(html_content, 'html')
    message.attach(msg)

    if attachment_path and attachment_name:
        try:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEApplication(attachment.read(), _subtype="gpx")
                part.add_header('Content-Disposition', 'attachment', filename=attachment_name)
                message.attach(part)
        except Exception as e:
            logger.error(f"Error attaching file: {e}")

    return message

def send_gmail_message(sender_info, message):
    """Send an email message using SMTP."""
    try:
        if not sender_info:
            logger.error("No sender information provided")
            return False

        gmail_user = sender_info['user']
        gmail_password = sender_info['password']

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)

        server.send_message(message)
        server.close()

        logger.info(f'Email sent successfully to {message["to"]}')
        return True
    except Exception as e:
        logger.error(f'An error occurred while sending email: {e}')
        return False