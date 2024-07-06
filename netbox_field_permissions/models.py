import logging
from typing import List, Tuple, Union

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from utilities.querysets import RestrictedQuerySet

from netbox_field_permissions.constants import (
    FIELDPERMISSION_IGNORE_FIELD_NAMES,
    FIELDPERMISSION_IGNORE_FIELD_TYPES,
    FIELDPERMISSION_OBJECT_TYPES,
)

logger = logging.getLogger(__name__)


class ObjectAbsoluteUrlMixin:
    def get_absolute_url(self):
        path = f"plugins:{self._meta.app_label}:{self._meta.model_name}"
        return reverse(path, args=[self.pk])


class FieldPermission(ObjectAbsoluteUrlMixin, models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    enabled = models.BooleanField(default=True)
    content_type = models.ForeignKey(
        to="core.ObjectType",
        on_delete=models.CASCADE,
        limit_choices_to=FIELDPERMISSION_OBJECT_TYPES,
        related_name="+",
        verbose_name="Object Type",
    )
    groups = models.ManyToManyField(to="users.Group", blank=True, related_name="+")
    users = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, blank=True, related_name="+"
    )
    actions = ArrayField(
        base_field=models.CharField(max_length=30),
        help_text=_("The list of fields and action denied by this permission"),
        null=True,
        default=list,
    )

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"

    def get_model_fields(self) -> Union[List[Tuple[str, str]], None]:
        if not self.content_type:
            return None

        model: models.Model = self.content_type.model_class()
        model_fields = model._meta.get_fields()

        fields = list()
        for field in model_fields:
            if (
                isinstance(field, FIELDPERMISSION_IGNORE_FIELD_TYPES)
                or field.name in FIELDPERMISSION_IGNORE_FIELD_NAMES
                or field.name.startswith("_")
            ):
                continue

            fields.append((field.name, field.name.replace("_", " ").title()))

        return fields
