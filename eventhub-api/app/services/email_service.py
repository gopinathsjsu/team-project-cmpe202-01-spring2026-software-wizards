"""
Email service — sends HTML emails via SMTP using Python stdlib.
All sends are fire-and-forget: wrap in asyncio.create_task() in callers.
"""
import asyncio
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import get_settings
from app.services.notification_service import BaseNotification

logger = logging.getLogger(__name__)
settings = get_settings()


class EmailService:
    def _send_sync(self, notification: BaseNotification) -> None:
        """Blocking SMTP send — run in executor to avoid blocking event loop."""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = notification.subject()
        msg["From"] = settings.SMTP_FROM
        msg["To"] = notification.to_email()
        msg.attach(MIMEText(notification.html_body(), "html"))

        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.ehlo()
                server.starttls()
                if settings.SMTP_USER:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM, notification.to_email(), msg.as_string())
            logger.info("Email sent to %s: %s", notification.to_email(), notification.subject())
        except Exception as exc:
            logger.error("Failed to send email to %s: %s", notification.to_email(), exc)

    async def send(self, notification: BaseNotification) -> None:
        """Async wrapper — runs SMTP in a thread pool to avoid blocking."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._send_sync, notification)


email_service = EmailService()
