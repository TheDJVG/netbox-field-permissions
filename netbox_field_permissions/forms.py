from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from netbox.forms import NetBoxModelForm
from utilities.forms.rendering import FieldSet

from netbox_field_permissions.constants import FIELDPERMISSION_FIELD_ACTIONS
from netbox_field_permissions.models import FieldPermission


class FieldPermissionEditForm(NetBoxModelForm):
    fieldsets = (
        FieldSet("name", "description", "enabled"),
        FieldSet("users", "groups", name="Assignment"),
    )

    class Meta:
        model = FieldPermission
        fields = ("name", "description", "enabled", "users", "groups")

    def __init__(self, *args, **kwargs):
        self.field_permission_fields = {}
        self.field_permission_initial = defaultdict(list)

        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self._set_initial_model_fields()
            self._append_model_fields()
            self._update_fieldsets()

    def _set_initial_model_fields(self):
        for action in self.instance.actions:
            field, action = action.split(":")
            self.field_permission_initial[field].append(action)

    def _append_model_fields(self):
        fields = self.instance.get_model_fields()
        for field in fields:
            # FIXME: Try to get label from actual NetBox form for consistent naming.
            name, label = field
            field_name = f"_fp_{name}"
            self.fields[field_name] = forms.MultipleChoiceField(
                choices=FIELDPERMISSION_FIELD_ACTIONS,
                required=False,
                initial=self.field_permission_initial.get(name),
                label=label,
            )
            self.field_permission_fields[field_name] = name

    def _update_fieldsets(self):
        self.fieldsets = (
            *self.fieldsets,
            FieldSet(
                *self.field_permission_fields.keys(),
                name=f"Deny actions on fields for '{self.instance.content_type}'",
            ),
        )

    def clean(self):
        self.instance.actions = []

        for form_field_name, model_field_name in self.field_permission_fields.items():
            field_actions = self.cleaned_data.get(form_field_name)
            for action in field_actions:
                self.instance.actions.append(f"{model_field_name}:{action}")

        if self.instance.pk and not self.instance.actions:
            raise ValidationError("At least one field action must be selected.")

        return super().clean()


class FieldPermissionForm(NetBoxModelForm):
    fieldsets = (
        FieldSet("name", "description", "enabled"),
        FieldSet("content_type", name="Restrictions"),
        FieldSet("users", "groups", name="Assignment"),
    )

    class Meta:
        model = FieldPermission
        fields = ("name", "description", "enabled", "content_type", "users", "groups")
