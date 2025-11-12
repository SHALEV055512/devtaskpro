# =============================================================
# SEND AUTH EMAIL (Verification or Password Reset)
# =============================================================

from mail.send_email import send_email
from mail.email_verification_manager import save_token
import random, time

# =============================================================
# TOKEN GENERATION
# =============================================================

def generate_token():
    """Generates a 6-digit random verification token"""
    return str(random.randint(100000, 999999))


# =============================================================
# SEND AUTH EMAIL
# =============================================================

def send_auth_email(receiver_email: str, user_data: dict | None = None):
    """
    Sends either a verification email (on registration)
    or a password reset email (on forgot password)
    """
    token = generate_token()
    created_at = time.time()
    expires_in = 10 * 60  # 10 minutes

    # === DETERMINE EMAIL TYPE ===
    if user_data:
        # Registration verification
        subject = "Verify your DevTaskPro account"
        title = "Email Verification"
        body_text = (
            "To complete your registration, please use the following verification code:"
        )
        color = "#007bff"
        print_type = "Verification"
    else:
        # Password reset
        subject = "Reset your DevTaskPro password"
        title = "Password Reset Request"
        body_text = (
            "To reset your password, please use the following code:"
        )
        color = "#d9534f"
        print_type = "Password Reset"

    # === EMAIL CONTENT ===
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 20px;">
        <div style="max-width: 500px; margin: auto; background-color: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
          <h2 style="color: #0b5394; text-align: center;">{title}</h2>
          <p style="font-size: 16px;">Hello,</p>
          <p style="font-size: 16px;">{body_text}</p>
          <h1 style="text-align: center; color: {color}; letter-spacing: 4px;">{token}</h1>
          <p style="font-size: 14px; color: #666;">This code is valid for <strong>10 minutes</strong>. 
          If you didn’t request this, you can safely ignore this email.</p>
          <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">
          <p style="font-size: 12px; color: #aaa; text-align: center;">© 2025 DevTaskPro | All rights reserved.</p>
        </div>
      </body>
    </html>
    """

    # === SEND EMAIL ===
    send_email(receiver_email, subject, html_content)

    # === SAVE TOKEN ===
    save_token(receiver_email, token, user_data or {}, expires_in)

    # === DEBUG INFO ===
    print(f"✅ {print_type} email sent to {receiver_email}")
    print(f"🔑 Token: {token} (valid for 10 minutes)")

    return token
