"""Reusable filter foundations."""

from __future__ import annotations

import django_filters


class BaseFilter(django_filters.FilterSet):
    """Base class for feature filters.

    Feature filters define allowed fields explicitly in their concrete classes.
    """

    class Meta:
        abstract = True
