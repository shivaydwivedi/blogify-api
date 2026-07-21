"""Reusable pagination foundations."""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.common.responses import APIResponse


class BasePagination(PageNumberPagination):
    """Default page-number pagination for API collections."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data) -> Response:
        return APIResponse.paginated(
            data=data,
            pagination={
                "page": self.page.number,
                "page_size": self.get_page_size(self.request),
                "total_count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
        )
