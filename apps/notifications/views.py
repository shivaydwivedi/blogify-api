"""Views for notification APIs."""

from __future__ import annotations

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions

from apps.common.api import BaseAPIView, BasePagination
from apps.notifications.models import Notification
from apps.notifications.serializers import (
    NotificationListSerializer,
    NotificationUpdateSerializer,
)


@extend_schema(tags=["Notifications"])
class NotificationListAPIView(BaseAPIView):
    """List the authenticated user's notifications."""

    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BasePagination
    serializer_class = NotificationListSerializer

    def get(self, request):
        queryset = (
            Notification.objects.filter(recipient=request.user)
            .select_related("actor", "recipient", "related_post", "related_comment")
            .order_by("-created_at")
        )
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.serializer_class(
            page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


@extend_schema(tags=["Notifications"])
class NotificationReadAPIView(BaseAPIView):
    """Mark a single notification as read."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NotificationUpdateSerializer

    @extend_schema(request=None, responses={200: NotificationListSerializer})
    def patch(self, request, pk):
        notification = get_object_or_404(
            Notification.objects.filter(recipient=request.user),
            pk=pk,
        )
        notification.is_read = True
        notification.save(update_fields=("is_read", "updated_at"))
        return self.success_response(
            NotificationListSerializer(
                notification,
                context={"request": request},
            ).data,
        )


@extend_schema(tags=["Notifications"])
class NotificationReadAllAPIView(BaseAPIView):
    """Mark all notifications for the authenticated user as read."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NotificationUpdateSerializer

    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(description="Notifications marked as read.")},
    )
    def patch(self, request):
        updated_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        ).update(is_read=True)
        return self.success_response({"updated_count": updated_count})
