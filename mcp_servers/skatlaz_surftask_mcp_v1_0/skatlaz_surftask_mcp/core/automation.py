from __future__ import annotations
import smtplib, ssl
from email.message import EmailMessage

def send_email_smtp(host: str, port: int, username: str, password: str, to: str, subject: str, body: str, use_tls: bool = True) -> dict:
    msg = EmailMessage()
    msg["From"] = username
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    context = ssl.create_default_context()
    if use_tls:
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(host, port) as server:
            server.starttls(context=context)
            server.login(username, password)
            server.send_message(msg)
    return {"sent": True, "to": to, "subject": subject}
