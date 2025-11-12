# =============================================================
# TEST: FULL PASSWORD RESET FLOW (FINAL VERSION)
# =============================================================

from mail.forgot_password import (
    request_password_reset,
    verify_reset_token,
    reset_password
)


def main():
    print("\n🧩 STEP 1: REQUEST PASSWORD RESET")
    email = input("👉 Enter your email: ").strip()

    # שולח את מייל האיפוס בפועל
    result = request_password_reset(email)
    print(f"\n📤 Output: {result['message']}")

    if not result.get("success"):
        print("❌ Failed to send reset email.")
        return

    # =============================================================
    # STEP 2: VERIFY TOKEN
    # =============================================================
    print("\n📧 Check your inbox for the 6-digit code.")
    token = input("🔑 Enter the token you received: ").strip()

    verify_result = verify_reset_token(email, token)
    print(f"\n🧠 Token verification result: {verify_result['message']}")

    if not verify_result["success"]:
        print("❌ Invalid or expired token. Exiting.")
        return

    # =============================================================
    # STEP 3: ENTER NEW PASSWORD
    # =============================================================
    new_password = input("\n🔒 Enter your new password: ").strip()

    reset_result = reset_password(email, new_password)
    print(f"\n🔁 Password reset result: {reset_result['message']}")

    if not reset_result["success"]:
        print("❌ Password reset failed.")
        return

    print("\n✅ Password reset flow completed successfully!")
    print("🎉 PASSWORD RESET FLOW COMPLETE 🎉")


if __name__ == "__main__":
    main()
