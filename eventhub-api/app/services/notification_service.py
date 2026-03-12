"""
Factory Pattern — NotificationFactory maps NotificationType → concrete notification class.
Each notification type encapsulates its own email subject and HTML body.
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.event import Event
    from app.models.registration import Registration


class NotificationType(Enum):
    REGISTRATION_CONFIRMATION = "registration_confirmation"
    REGISTRATION_CANCELLATION = "registration_cancellation"
    EVENT_CANCELLATION = "event_cancellation"
    EVENT_APPROVED = "event_approved"
    EVENT_REJECTED = "event_rejected"
    EVENT_REMINDER = "event_reminder"
    PASSWORD_RESET = "password_reset"


class BaseNotification(ABC):
    """Abstract base for all notification types (Factory Pattern)."""

    @abstractmethod
    def subject(self) -> str: ...

    @abstractmethod
    def html_body(self) -> str: ...

    def to_email(self) -> str:
        """Return the recipient email address."""
        raise NotImplementedError


class RegistrationConfirmationNotification(BaseNotification):
    def __init__(self, user: "User", registration: "Registration", event: "Event"):
        self.user = user
        self.registration = registration
        self.event = event

    def subject(self) -> str:
        return f"Your ticket for {self.event.title}"

    def html_body(self) -> str:
        return f"""
        <h1>You're registered!</h1>
        <p>Hi {self.user.first_name},</p>
        <p>Your registration for <strong>{self.event.title}</strong> is confirmed.</p>
        <p><strong>Date:</strong> {self.event.start_at.strftime('%B %d, %Y at %I:%M %p %Z')}</p>
        <p><strong>Venue:</strong> {self.event.venue_name or 'Virtual Event'}</p>
        <p><strong>Tickets:</strong> {self.registration.quantity} × {self.registration.ticket_type.name if hasattr(self.registration, 'ticket_type') and self.registration.ticket_type else 'General'}</p>
        <p><strong>QR Token:</strong> {self.registration.qr_token}</p>
        <p><strong>Reference:</strong> {self.registration.payment_ref or 'N/A'}</p>
        <hr/>
        <p>See you there! — EventHub Team</p>
        """

    def to_email(self) -> str:
        return self.user.email


class RegistrationCancellationNotification(BaseNotification):
    def __init__(self, user: "User", registration: "Registration", event: "Event"):
        self.user = user
        self.registration = registration
        self.event = event

    def subject(self) -> str:
        return f"Registration cancelled: {self.event.title}"

    def html_body(self) -> str:
        return f"""
        <h1>Registration Cancelled</h1>
        <p>Hi {self.user.first_name},</p>
        <p>Your registration for <strong>{self.event.title}</strong> has been cancelled.</p>
        <p>If you paid for tickets, a refund will be processed within 5–7 business days.</p>
        <hr/>
        <p>EventHub Team</p>
        """

    def to_email(self) -> str:
        return self.user.email


class EventCancellationNotification(BaseNotification):
    def __init__(self, user: "User", event: "Event"):
        self.user = user
        self.event = event

    def subject(self) -> str:
        return f"Event cancelled: {self.event.title}"

    def html_body(self) -> str:
        return f"""
        <h1>Event Cancelled</h1>
        <p>Hi {self.user.first_name},</p>
        <p>We're sorry to inform you that <strong>{self.event.title}</strong> has been cancelled.</p>
        <p>Your registration has been automatically cancelled and any payments will be refunded.</p>
        <hr/>
        <p>EventHub Team</p>
        """

    def to_email(self) -> str:
        return self.user.email


class EventApprovedNotification(BaseNotification):
    def __init__(self, user: "User", event: "Event"):
        self.user = user
        self.event = event

    def subject(self) -> str:
        return f"Your event has been approved: {self.event.title}"

    def html_body(self) -> str:
        return f"""
        <h1>Event Approved!</h1>
        <p>Hi {self.user.first_name},</p>
        <p>Great news! Your event <strong>{self.event.title}</strong> has been approved and is now live.</p>
        <p>Attendees can now register for your event.</p>
        <hr/>
        <p>EventHub Team</p>
        """

    def to_email(self) -> str:
        return self.user.email


class EventRejectedNotification(BaseNotification):
    def __init__(self, user: "User", event: "Event", reason: str = ""):
        self.user = user
        self.event = event
        self.reason = reason

    def subject(self) -> str:
        return f"Your event was not approved: {self.event.title}"

    def html_body(self) -> str:
        reason_html = f"<p><strong>Reason:</strong> {self.reason}</p>" if self.reason else ""
        return f"""
        <h1>Event Not Approved</h1>
        <p>Hi {self.user.first_name},</p>
        <p>Unfortunately, your event <strong>{self.event.title}</strong> was not approved at this time.</p>
        {reason_html}
        <p>You may update your event and re-submit for review.</p>
        <hr/>
        <p>EventHub Team</p>
        """

    def to_email(self) -> str:
        return self.user.email


class EventReminderNotification(BaseNotification):
    def __init__(self, user: "User", event: "Event"):
        self.user = user
        self.event = event

    def subject(self) -> str:
        return f"Reminder: {self.event.title} is tomorrow!"

    def html_body(self) -> str:
        return f"""
        <h1>Event Reminder</h1>
        <p>Hi {self.user.first_name},</p>
        <p>This is a reminder that <strong>{self.event.title}</strong> is happening in approximately 48 hours.</p>
        <p><strong>Date:</strong> {self.event.start_at.strftime('%B %d, %Y at %I:%M %p %Z')}</p>
        <p><strong>Venue:</strong> {self.event.venue_name or 'Virtual Event'}</p>
        <hr/>
        <p>See you there! — EventHub Team</p>
        """

    def to_email(self) -> str:
        return self.user.email


class PasswordResetNotification(BaseNotification):
    def __init__(self, user: "User", reset_link: str):
        self.user = user
        self.reset_link = reset_link

    def subject(self) -> str:
        return "Reset your EventHub password"

    def html_body(self) -> str:
        return f"""
        <h1>Password Reset Request</h1>
        <p>Hi {self.user.first_name},</p>
        <p>Click the link below to reset your password. This link expires in 1 hour.</p>
        <p><a href="{self.reset_link}" style="background:#3b82f6;color:#fff;padding:12px 24px;border-radius:6px;text-decoration:none;">Reset Password</a></p>
        <p>If you did not request a password reset, you can ignore this email.</p>
        <hr/>
        <p>EventHub Team</p>
        """

    def to_email(self) -> str:
        return self.user.email


class NotificationFactory:
    """
    Factory Pattern — creates the correct notification object from a NotificationType enum.
    New notification types can be added by registering them in _registry.
    """
    _registry: Dict[NotificationType, Type[BaseNotification]] = {
        NotificationType.REGISTRATION_CONFIRMATION: RegistrationConfirmationNotification,
        NotificationType.REGISTRATION_CANCELLATION: RegistrationCancellationNotification,
        NotificationType.EVENT_CANCELLATION: EventCancellationNotification,
        NotificationType.EVENT_APPROVED: EventApprovedNotification,
        NotificationType.EVENT_REJECTED: EventRejectedNotification,
        NotificationType.EVENT_REMINDER: EventReminderNotification,
        NotificationType.PASSWORD_RESET: PasswordResetNotification,
    }

    @classmethod
    def create(cls, ntype: NotificationType, **kwargs) -> BaseNotification:
        klass = cls._registry.get(ntype)
        if not klass:
            raise ValueError(f"Unknown notification type: {ntype}")
        return klass(**kwargs)