import django_tables2 as table
from netbox.tables import BaseTable, NetBoxTable, columns

from netbox_field_permissions.models import FieldPermission


class ArrayColumn(table.Column):
    def render(self, value):
        if value:
            return ", ".join(value)
        return value


class FieldPermissionListTable(NetBoxTable):
    name = table.Column(linkify=True)
    _actions = ArrayColumn(accessor="actions")  # Actions is also used by NetBoxTable.
    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = FieldPermission
        fields = (
            "id",
            "name",
            "enabled",
            "content_type",
            "users",
            "groups",
            "_actions",
            "description",
        )
        default_columns = (
            "name",
            "enabled",
            "content_type",
            "users",
            "groups",
            "_actions",
            "description",
        )


# Table to show which fields are restricted
class FieldPermissionTable(BaseTable):
    field = table.Column()
    add = table.BooleanColumn()
    change = table.BooleanColumn()

    class Meta(NetBoxTable.Meta):
        fields = ("field", "add", "change")


class FieldPermissionValidatorTable(BaseTable):
    model = table.Column()
    enabled = table.BooleanColumn(verbose_name="Validator Enabled")

    class Meta(NetBoxTable.Meta):
        fields = ("model", "enabled")
