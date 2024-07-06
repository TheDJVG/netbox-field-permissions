from netbox.plugins import PluginMenuButton, PluginMenuItem

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_field_permissions:fieldpermission_list",
        link_text="Field Permissions",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_field_permissions:fieldpermission_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=("netbox_field_permissions.add_fieldpermission",),
            )
        ],
    ),
)
