from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q
from utilities.fields import CounterCacheField, NaturalOrderingField

# Limit choices to common NetBox apps. Change this in the future if we want to support other plugin models too.
# FIXME: Source from netbox.registry.Registry (check migration compatibility)
FIELDPERMISSION_OBJECT_TYPES = Q(
    app_label__in=[
        "circuits",
        "extras",
        "ipam",
        "tenancy",
        "wireless",
        "dcim",
        "virtualization",
        "vpn",
    ]
)

# Ignore these field types as they're not used by the end-user directly (GUI/API)
FIELDPERMISSION_IGNORE_FIELD_TYPES = (
    GenericRelation,
    NaturalOrderingField,
    CounterCacheField,
)

# Ignore these fields as a) people don't have control over them b) shouldn't interfere with them.
FIELDPERMISSION_IGNORE_FIELD_NAMES = (
    "id",
    "pk",
    "created",
    "last_updated",
    "custom_field_data",
)

FIELDPERMISSION_FIELD_ACTIONS = (("add", "Add"), ("change", "Change"))

FIELDPERMISSION_VALIDATOR = (
    "netbox_field_permissions.validators.FieldPermissionValidator"
)
