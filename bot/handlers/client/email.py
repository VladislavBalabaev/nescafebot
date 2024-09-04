import aiosmtplib
from email.message import EmailMessage

from configs.env_reader import config


async def send_email(email_to, text):
    message = EmailMessage()

    message["From"] = "madfure@gmail.com"
    message["To"] = email_to
    message["Subject"] = "Код подтверждения (NEScafeBot)"
    message.set_content(text)

    await aiosmtplib.send(
        message,
        username="madfure@gmail.com",
        password=config.EMAIL_PASSWORD.get_secret_value(),
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
    )
