import os
import smtplib
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# טוען את קובץ ההגדרות
load_dotenv("password_mail.env")

SENDER = os.getenv("GMAIL_USER")
APP_PASS = os.getenv("GMAIL_APP_PASSWORD")

# === פונקציה ליצירת טוקן אקראי בן 6 ספרות ===
def generate_token():
    return str(random.randint(100000, 999999))

# === יצירת טוקן ושמירת זמן התחלה ===
token = generate_token()
created_at = time.time()
expires_in = 10 * 60  # 10 דקות (בשניות)

# === כתובת הנמען (לבדיקה נשלח לעצמנו) ===
receiver_email = SENDER

# === יצירת הודעת אימייל בעיצוב מקצועי ===
msg = MIMEMultipart("alternative")
msg["From"] = f"DevTaskPro Verification <{SENDER}>"
msg["To"] = receiver_email
msg["Subject"] = "Verify your DevTaskPro account"

html_content = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 20px;">
    <div style="max-width: 500px; margin: auto; background-color: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
      <h2 style="color: #0b5394; text-align: center;">Email Verification</h2>
      <p style="font-size: 16px;">Hello,</p>
      <p style="font-size: 16px;">To complete your registration, please use the following verification code:</p>
      <h1 style="text-align: center; color: #007bff; letter-spacing: 4px;">{token}</h1>
      <p style="font-size: 14px; color: #666;">This code is valid for <strong>10 minutes</strong>. If you didn’t request this, you can safely ignore this email.</p>
      <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">
      <p style="font-size: 12px; color: #aaa; text-align: center;">© 2025 DevTaskPro | All rights reserved.</p>
    </div>
  </body>
</html>
"""

msg.attach(MIMEText(html_content, "html"))

# === שליחת המייל ===
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER, APP_PASS)
        server.send_message(msg)
        print("✅ Verification email sent successfully!")
        print(f"🕒 Token: {token} (valid for 10 minutes)")
except Exception as e:
    print("❌ Error sending email:", e)

# === פונקציה לבדוק אם הטוקן עדיין בתוקף (לשימוש עתידי בבאקנד) ===
def is_token_valid(created_at, expires_in):
    return (time.time() - created_at) < expires_in
