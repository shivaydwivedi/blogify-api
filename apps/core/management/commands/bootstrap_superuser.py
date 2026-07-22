"""Create the initial production superuser when explicitly configured."""

from __future__ import annotations

import logging
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

SUPERUSER_ENV_VARS = (
    "DJANGO_SUPERUSER_USERNAME",
    "DJANGO_SUPERUSER_EMAIL",
    "DJANGO_SUPERUSER_PASSWORD",
)


class Command(BaseCommand):
    """Create a superuser from environment variables when none exists."""

    help = "Create the initial superuser from optional environment variables."

    def handle(self, *args, **options) -> None:
        user_model = get_user_model()

        if user_model.objects.filter(is_superuser=True).exists():
            self.log_message("Superuser already exists.")
            return

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        missing = [
            name
            for name, value in zip(
                SUPERUSER_ENV_VARS,
                (username, email, password),
                strict=True,
            )
            if not value
        ]
        if missing:
            self.log_message(
                "Skipping superuser creation. Missing environment variables: "
                f"{', '.join(missing)}"
            )
            return

        user_model.objects.create_superuser(
            email=email,
            username=username,
            password=password,
        )
        self.log_message("Superuser created successfully.")

    def log_message(self, message: str) -> None:
        logger.info(message)
        self.stdout.write(message)
