from __future__ import annotations

import uuid

import pytest
from django.contrib.auth import get_user_model
from django.db import connection, models
from django.utils import timezone

from apps.common.models import BaseModel


class FrameworkModel(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "tests"


@pytest.fixture
def framework_model_table(transactional_db):
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(FrameworkModel)

    try:
        yield FrameworkModel
    finally:
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(FrameworkModel)


@pytest.mark.django_db
def test_base_model_uses_uuid_primary_key(framework_model_table) -> None:
    record = framework_model_table.objects.create(name="Example")

    assert isinstance(record.id, uuid.UUID)


@pytest.mark.django_db
def test_timestamped_model_sets_created_and_updated_timestamps(
    framework_model_table,
) -> None:
    record = framework_model_table.objects.create(name="Example")

    assert record.created_at is not None
    assert record.updated_at is not None
    assert timezone.is_aware(record.created_at)
    assert timezone.is_aware(record.updated_at)


@pytest.mark.django_db
def test_soft_delete_hides_record_from_default_manager(framework_model_table) -> None:
    record = framework_model_table.objects.create(name="Example")

    deleted_count, deleted_detail = record.delete()

    assert deleted_count == 1
    assert deleted_detail == {"tests.FrameworkModel": 1}
    assert framework_model_table.objects.count() == 0
    assert framework_model_table.deleted_objects.count() == 1
    assert framework_model_table.all_objects.count() == 1

    record.refresh_from_db()
    assert record.is_deleted is True
    assert record.deleted_at is not None


@pytest.mark.django_db
def test_soft_deleted_record_can_be_restored(framework_model_table) -> None:
    record = framework_model_table.objects.create(name="Example")
    record.soft_delete()

    record.restore()

    record.refresh_from_db()
    assert record.is_deleted is False
    assert record.deleted_at is None
    assert framework_model_table.objects.count() == 1


@pytest.mark.django_db
def test_hard_delete_removes_record(framework_model_table) -> None:
    record = framework_model_table.objects.create(name="Example")

    deleted_count, deleted_detail = record.delete(hard=True)

    assert deleted_count == 1
    assert deleted_detail == {"tests.FrameworkModel": 1}
    assert framework_model_table.all_objects.count() == 0


@pytest.mark.django_db
def test_audit_model_accepts_future_actor_references(framework_model_table) -> None:
    user_model = get_user_model()
    user = user_model.objects.create_user(username="auditor")

    record = framework_model_table.all_objects.create(
        name="Example",
        created_by=user,
        updated_by=user,
    )

    assert record.created_by == user
    assert record.updated_by == user
