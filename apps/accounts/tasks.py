"""Asynchronous account communication tasks."""

from __future__ import annotations

from urllib.parse import urlencode

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from apps.accounts.tokens import generate_email_verification_token


@shared_task(name="apps.accounts.tasks.send_verification_email")
def send_verification_email(user_id: str) -> bool:
    """Send an email verification message to a user."""

    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)

    if user.email_verified:
        return False

    token = generate_email_verification_token(user)
    verification_path = reverse("accounts:verify-email")
    verification_url = (
        f"{settings.BLOGIFY_API_BASE_URL.rstrip('/')}{verification_path}?"
        f"{urlencode({'token': token})}"
    )
    context = {
        "user": user,
        "verification_url": verification_url,
    }
    text_body = render_to_string("accounts/email/verify_account.txt", context)
    html_body = render_to_string("accounts/email/verify_account.html", context)

    email = EmailMultiAlternatives(
        subject="Verify your Blogify account",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send()
    return True
