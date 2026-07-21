"""Operational views for deployment readiness."""

from __future__ import annotations

from django.conf import settings
from django.db import connection
from drf_spectacular.utils import extend_schema
from redis import Redis
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):
    """Return application dependency health for platform checks."""

    authentication_classes: tuple = ()
    permission_classes: tuple = ()

    @extend_schema(exclude=True)
    def get(self, request):
        database_status = self.check_database()
        redis_status = self.check_redis()
        is_healthy = database_status == "ok" and redis_status == "ok"

        return Response(
            {
                "status": "healthy" if is_healthy else "unhealthy",
                "database": database_status,
                "redis": redis_status,
                "version": settings.APP_VERSION,
            },
            status=(
                status.HTTP_200_OK
                if is_healthy
                else status.HTTP_503_SERVICE_UNAVAILABLE
            ),
        )

    def check_database(self) -> str:
        try:
            connection.ensure_connection()
            return "ok"
        except Exception:
            return "error"

    def check_redis(self) -> str:
        try:
            client = Redis.from_url(
                settings.REDIS_URL,
                socket_connect_timeout=2,
                socket_timeout=2,
            )
            client.ping()
            return "ok"
        except Exception:
            return "error"
