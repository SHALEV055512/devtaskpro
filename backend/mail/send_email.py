# =============================================================
# SEND EMAIL MODULE
# =============================================================

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path

# =============================================================
# LOAD ENVIRONMENT VARIABLES
# =============================================================

load_dotenv(Path(__file__).resolve().parent / "password_mail.env")

SENDER = os.getenv("GMAIL_USER")
APP_PASS = os.getenv("GMAIL_APP_PASSWORD")


# =============================================================
# SEND EMAIL FUNCTION
# =============================================================

def send_email(receiver_email: str, subject: str, html_content: str):
    """Sends an HTML email to the specified address"""

    msg = MIMEMultipart("alternative")
    msg["From"] = f"DevTaskPro <{SENDER}>"
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER, APP_PASS)
            server.send_message(msg)
            print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print("Error sending email:", e)
