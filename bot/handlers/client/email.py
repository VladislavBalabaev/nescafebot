import asyncio
import aiosmtplib
from email.message import EmailMessage

async def send_email(email_to, text, code_number):
    # Create the email message
    message = EmailMessage()
    message["From"] = "madfure@gmail.com"
    message["To"] = email_to
    message["Subject"] = "Test Email"
    message.set_content(text + str(code_number))

    # Email server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = "madfure@gmail.com"
    password = "wqps fpna sfkq nbqg"

    # Send the email
    await aiosmtplib.send(
        message,
        hostname=smtp_server,
        port=smtp_port,
        start_tls=True,
        username=username,
        password=password
    )

# Run the send_email coroutine

if __name__ == "__main__":
    asyncio.run(send_email("bpletenev@nes.ru", "Here is your verification code: ", 148520))