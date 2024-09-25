import aiosmtplib
from random import choice
from email.message import EmailMessage

from configs.env_reader import config


emails = [
    {
        "email": "nes.cafe.user1@gmail.com",
        "password": config.EMAIL1_PASSWORD.get_secret_value()
    },
    {
        "email": "nes.cafe.user2@gmail.com",
        "password": config.EMAIL2_PASSWORD.get_secret_value()
    },
    {
        "email": "nes.cafe.user4@gmail.com",
        "password": config.EMAIL4_PASSWORD.get_secret_value()
    },
    {
        "email": "madfure@gmail.com",
        "password": config.EMAIL_MADFYRE_PASSWORD.get_secret_value()
    },
]


async def send_email(email_to, text):
    global emails

    email_sender = choice(emails)

    message = EmailMessage()
    message["Subject"] = "Код подтверждения (NEScafeBot)"
    message["From"] = email_sender["email"]
    message["To"] = email_to
    message.set_content(text)


    await aiosmtplib.send(
        message,
        username=email_sender["email"],
        password=email_sender["password"],
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
    )

    return
