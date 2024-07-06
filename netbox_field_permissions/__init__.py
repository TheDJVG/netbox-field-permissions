from netbox.plugins import PluginConfig


class NetBoxFieldPermissionsConfig(PluginConfig):
    name = "netbox_field_permissions"
    verbose_name = "Field Permissions"
    description = "Limit user/groups to change object field values"
    version = "0.1.0rc1"
    min_version = "4.0"
    author = "Daan van Gorkum"
    author_email = "me+netbox@dj.vg"
    default_settings = {
        "enabled": True,
    }


config = NetBoxFieldPermissionsConfig
