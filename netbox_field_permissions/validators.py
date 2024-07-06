from django.conf import settings
from django.core.exceptions import ValidationError
from extras.validators import CustomValidator

from netbox_field_permissions.utilities import get_disabled_fields

plugin_settings = settings.PLUGINS_CONFIG["netbox_field_permissions"]


class FieldPermissionValidator(CustomValidator):
    def validate(self, instance, request):
        if not plugin_settings["enabled"]:
            return False

        action = "change" if instance.pk else "add"
        model = instance.__class__

        # Superusers can always change fields.
        if request.user.is_superuser:
            return

        disabled_fields = get_disabled_fields(
            user=request.user, model=model, action=action
        )

        field_errors = {}
        if action == "add":
            for field in disabled_fields:
                if getattr(instance, field) is not None:
                    field_errors[field] = "No permission to set value"
        else:
            if hasattr(instance, "_prechange_snapshot"):
                snapshot = instance._prechange_snapshot
                current = instance.serialize_object()

                for field in disabled_fields:
                    if current[field] != snapshot[field]:
                        field_errors[field] = "No permission to change value"

        if field_errors:
            raise ValidationError(field_errors)
