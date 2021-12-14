"""Emailing of new tenant-to-tenant messages."""

from typing import Iterator

from emaillib import EMail
from functoolsplus import coerce
from notificationlib import get_email_func

from tenant2tenant.config import get_config
from tenant2tenant.orm import NotificationEmail


__all__ = ['email']


@coerce(frozenset)
def get_emails(message: str) -> Iterator[EMail]:
    """Yields notification emails."""

    for notification_email in NotificationEmail.select().where(
            NotificationEmail.customer == message.customer):
        recipient = notification_email.email
        sender = (config := get_config()).get('email', 'from')
        subject = notification_email.subject or config.get('email', 'subject')
        subject = subject.format(address=message.address)
        html = message.message if notification_email.html else None
        plain = None if notification_email.html else message.message
        yield EMail(subject, sender, recipient, plain=plain, html=html)


email = get_email_func(get_emails)  # pylint: disable=C0103
