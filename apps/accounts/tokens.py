"""Email verification token helpers."""

from __future__ import annotations

from django.conf import settings
from django.core import signing

EMAIL_VERIFICATION_SALT = "apps.accounts.email_verification"


def generate_email_verification_token(user) -> str:
    """Create a signed email verification token for a user."""

    return signing.dumps(
        {"user_id": str(user.id), "email": user.email},
        salt=EMAIL_VERIFICATION_SALT,
    )


def load_email_verification_token(token: str) -> dict[str, str]:
    """Load and validate a signed email verification token."""

    return signing.loads(
        token,
        salt=EMAIL_VERIFICATION_SALT,
        max_age=settings.EMAIL_VERIFICATION_TOKEN_MAX_AGE_SECONDS,
    )
