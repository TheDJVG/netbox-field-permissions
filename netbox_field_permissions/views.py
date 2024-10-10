from collections import defaultdict

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from netbox.views.generic import (
    ObjectDeleteView,
    ObjectEditView,
    ObjectListView,
    ObjectView,
)

from netbox_field_permissions.constants import FIELDPERMISSION_VALIDATOR
from netbox_field_permissions.forms import FieldPermissionEditForm, FieldPermissionForm
from netbox_field_permissions.models import FieldPermission
from netbox_field_permissions.tables import (
    FieldPermissionListTable,
    FieldPermissionTable,
    FieldPermissionValidatorTable,
)
from netbox_field_permissions.utilities import (
    get_content_types_for_validator,
    install_validator,
    uninstall_validator,
    validator_status_by_content_type,
)

#
# FieldPermission
#


class FieldPermissionListView(ObjectListView):
    queryset = FieldPermission.objects.all()
    actions = {"add": {"add"}}
    table = FieldPermissionListTable
    template_name = "netbox_field_permissions/fieldpermission_list.html"


class FieldPermissionView(ObjectView):
    queryset = FieldPermission.objects.all()

    def get_extra_context(self, request, instance):
        # FIXME optimization, this is too dirty
        actions = ("add", "change")
        field_permissions = defaultdict(list)
        for action in instance.actions:
            field, action = action.split(":")
            field_permissions[field].append(action)

        fields = instance.get_model_fields()
        table_data = []

        for field in fields:
            name, label = field
            data = {"field": label}

            for action in actions:
                data[action] = False if action in field_permissions[name] else True
            table_data.append(data)

        return {
            "field_permission_table": FieldPermissionTable(
                data=table_data, empty_text="No fields defined for model"
            )
        }


class FieldPermissionEditView(ObjectEditView):
    queryset = FieldPermission.objects.all()
    template_name = "netbox_field_permissions/fieldpermission_edit.html"

    # Return different form is PK has been set.
    # This is because we need different fields based on the content_type.
    def form(self, instance, *args, **kwargs):
        if not instance.pk:
            return FieldPermissionForm(instance=instance, *args, **kwargs)

        return FieldPermissionEditForm(instance=instance, *args, **kwargs)


class FieldPermissionDeleteView(ObjectDeleteView):
    queryset = FieldPermission.objects.all()


class FieldPermissionManageView(UserPassesTestMixin, TemplateView):
    template_name = "netbox_field_permissions/manage.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        status = validator_status_by_content_type()

        # Create install/uninstall JSON for ease of use.
        current_validators = getattr(settings, "CUSTOM_VALIDATORS", {})

        # Dict for installing validators
        install_validators = current_validators.copy()
        for ct in get_content_types_for_validator():
            if ct not in install_validators:
                install_validators[ct] = (FIELDPERMISSION_VALIDATOR,)
            else:
                if FIELDPERMISSION_VALIDATOR not in install_validators[ct]:
                    install_validators[ct] = tuple(install_validators[ct]) + (
                        FIELDPERMISSION_VALIDATOR,
                    )

        # Dict for uninstalling validators
        uninstall_validators = current_validators.copy()
        for model, validator in uninstall_validators.copy().items():
            if FIELDPERMISSION_VALIDATOR not in validator:
                continue

            # If there's only 1 validator defined just remove the key from the config
            # so we don't end up with empty values.
            if len(validator) == 1:
                del uninstall_validators[model]
            else:
                uninstall_validators[model] = (
                    x for x in validator if x != FIELDPERMISSION_VALIDATOR
                )

        return {
            "validators_statically_configured": hasattr(settings, "CUSTOM_VALIDATORS"),
            "show_manual_install": "manual_install" in self.request.GET,
            "install_validators": install_validators,
            "uninstall_validators": uninstall_validators,
            "tables": {
                k: FieldPermissionValidatorTable(data=v, empty_text="No models in app")
                for k, v in status.items()
            },
        }

    def post(self, request, *args, **kwargs):
        if "_uninstall" in request.POST:
            uninstall_validator()
            messages.success(request, "Field Permissions Validator uninstalled")
        else:
            install_validator()
            messages.success(request, "Field Permissions Validator installed")

        return redirect("plugins:netbox_field_permissions:fieldpermission_manage")
