import aiosmtplib
from random import choice
from email.message import EmailMessage
from aiosmtplib.errors import SMTPAuthenticationError

from create_bot import bot
from configs.env_reader import config
from configs.selected_ids import ADMINS


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
]


async def send_email(email_to, text):
    global emails

    try:
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
    except SMTPAuthenticationError:
        send_email(email_to, text)
        return


async def test_emails():
    global emails
    
    for email_sender in emails:
        try:
            message = EmailMessage()
            message["Subject"] = "Проверка работоспособности (NEScafeBot)"
            message["From"] = email_sender["email"]
            message["To"] = "vbalabaev@nes.ru"
            message.set_content("Почта работает.")


            await aiosmtplib.send(
                message,
                username=email_sender["email"],
                password=email_sender["password"],
                hostname="smtp.gmail.com",
                port=587,
                start_tls=True,
            )

        except SMTPAuthenticationError:
            for admin in ADMINS:
                await bot.send_message(admin, f"WARNING: Email \"{email_sender['email']}\" is not working")

    return
