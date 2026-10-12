
import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_reset_otp(recipient_email: str, otp: str) -> None:
    sender = os.getenv("SMTP_EMAIL", "").strip()
    app_password = os.getenv("SMTP_APP_PASSWORD", "").replace(" ", "")

    if not sender or not app_password:
        raise RuntimeError("SMTP_EMAIL or SMTP_APP_PASSWORD is missing")

    message = EmailMessage()
    message["Subject"] = "Password Reset OTP - Teckinfo Support Assistant"
    message["From"] = sender
    message["To"] = recipient_email
    message.set_content(
        f"Your password reset OTP is: {otp}\n\n"
        "This OTP expires in 5 minutes. Do not share it with anyone."
    )

    context = ssl.create_default_context()

    # Try Gmail using SSL on port 465
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender, app_password)
        server.send_message(message)