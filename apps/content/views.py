"""ViewSets for content taxonomy APIs."""

from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, mixins, status

from apps.common.api import BasePagination, BaseViewSet
from apps.common.responses import APIResponse
from apps.content.models import Category, Tag
from apps.content.permissions import IsStaffOrReadOnly
from apps.content.serializers import CategorySerializer, TagSerializer


class TaxonomyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """Shared CRUD behavior for taxonomy resources."""

    permission_classes = (IsStaffOrReadOnly,)
    pagination_class = BasePagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    ordering = ("name",)
    ordering_fields = ("name", "created_at", "updated_at")
    search_fields = ("name", "slug")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return self.success_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return self.success_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.success_response(
            serializer.data,
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.success_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return APIResponse.empty()


@extend_schema(tags=["Categories"])
class CategoryViewSet(TaxonomyViewSet):
    """CRUD API for categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ("is_active",)
    search_fields = ("name", "slug", "description")


@extend_schema(tags=["Tags"])
class TagViewSet(TaxonomyViewSet):
    """CRUD API for tags."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
