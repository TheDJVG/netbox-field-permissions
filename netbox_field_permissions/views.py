from collections import defaultdict

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

from netbox_field_permissions.forms import FieldPermissionEditForm, FieldPermissionForm
from netbox_field_permissions.models import FieldPermission
from netbox_field_permissions.tables import (
    FieldPermissionListTable,
    FieldPermissionTable,
    FieldPermissionValidatorTable,
)
from netbox_field_permissions.utilities import (
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
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        status = validator_status_by_content_type()

        return {
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
