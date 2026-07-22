"""Create the initial production superuser when explicitly configured."""

from __future__ import annotations

import logging
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Create a superuser from environment variables when none exists."""

    help = "Create the initial superuser from optional environment variables."

    def handle(self, *args, **options) -> None:
        user_model = get_user_model()

        if user_model.objects.filter(is_superuser=True).exists():
            self.log_message("Superuser already exists.")
            return

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not email or not password:
            self.log_message("Skipping superuser creation.")
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
