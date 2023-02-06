import random
import smtplib
import string
from datetime import timedelta
from email.mime.text import MIMEText

from core.redisdb.redisdb import async_redis
from core.settings import settings


async def send_verify_on_email(email: str, username: str, uid: int):

    if settings.TESTING:
        return

    letters = string.ascii_lowercase
    key_for_verify = uid
    val_for_varify = "".join(random.choice(letters) for _ in range(20))
    link: str = (
        "http://"
        + settings.HOST
        + ":"
        + str(settings.PORT)
        + f"/user/v1/verify-email/{key_for_verify}/{val_for_varify}"
    )

    to = [
        email,
    ]
    subject = "Confirm your email for FastTube"
    email_text = f"""
    <h3>Hi, {username}</h3>
    <p>This email was sent to you to confirm this email.</p>
    <p>To confirm, follow the <a href="{link}">link</a></p>
    <p>If you have not registered on our service, then ignore this email.</p> 
    <p>Thanks</p>"""

    try:
        server_ssl = smtplib.SMTP_SSL("smtp.mail.ru", 465)
        server_ssl.login(user=settings.MAIL_USER, password=settings.MAIL_PASSWORD)
        mess = MIMEText(email_text, "html", _charset="utf-8")
        mess["From"] = settings.MAIL_USER
        mess["To"] = email
        mess["Subject"] = subject
        server_ssl.sendmail(settings.MAIL_USER, to, mess.as_string())
        redis_ = await async_redis.get_async_redis()
        await redis_.setex(key_for_verify, timedelta(minutes=30), value=val_for_varify)

    except Exception as e:
        print(e)
