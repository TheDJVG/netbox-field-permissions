# netbox-field-permissions

Limit the ability for user/groups to change certain fields on NetBox objects.

By default, NetBox only allows you to restrict access an individual object, with this plugin you can restrict access on a field of an object.

A common use case for this is compliance where certain information is not allowed to be altered or simply prevent accidental changes.
## Compatibility

| NetBox Version | Plugin Version |
|----------------|----------------|
| 4.0, 4.1       | 0.1.X          |

## Installing

For adding to a NetBox Docker setup see
[the general instructions for using netbox-docker with plugins](https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins).

### Install

```bash
pip install netbox-field-permissions
```

or by adding to your `local_requirements.txt` or `plugin_requirements.txt` (netbox-docker):

```bash
netbox-field-permissions
```

### Development Install

If you would like to install a version not yet published to pypi.

```bash
pip install git+https://github.com/TheDJVG/netbox-field-permissions
```

or by adding to your `local_requirements.txt` or `plugin_requirements.txt` (netbox-docker):

```bash
git+https://github.com/TheDJVG/netbox-field-permissions
```

### NetBox Configuration

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`,
or if you use netbox-docker, your `/configuration/plugins.py` file :

```python
PLUGINS = [
    'netbox_field_permissions'
]
```

### Validator installation
By default, the migration will install the validator for all models. If you're using a statically configured NetBox
instance you can use this `CUSTOM_VALIDATORS` block to install it for all models:
<details>
<summary>Show configuration snippet</summary>

```python
CUSTOM_VALIDATORS = {
    "circuits.circuit": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "circuits.circuittermination": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "circuits.circuittype": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "circuits.provider": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "circuits.provideraccount": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "circuits.providernetwork": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.cable": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.cablepath": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.cabletermination": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.consoleport": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.consoleporttemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.consoleserverport": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.consoleserverporttemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.device": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.devicebay": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.devicebaytemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.devicerole": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.devicetype": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.frontport": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.frontporttemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.interface": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.interfacetemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.inventoryitem": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.inventoryitemrole": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.inventoryitemtemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.location": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.manufacturer": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.module": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.modulebay": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.modulebaytemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.moduletype": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.platform": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.powerfeed": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.poweroutlet": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.poweroutlettemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.powerpanel": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.powerport": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.powerporttemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.rack": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.rackreservation": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.rackrole": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.rearport": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.rearporttemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.region": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.site": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.sitegroup": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.virtualchassis": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "dcim.virtualdevicecontext": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.bookmark": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.branch": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.cachedvalue": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.configcontext": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.configtemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.customfield": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.customfieldchoiceset": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.customlink": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.dashboard": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.eventrule": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.exporttemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.imageattachment": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.journalentry": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.objectchange": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.reportmodule": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.savedfilter": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.script": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.scriptmodule": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.stagedchange": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.tag": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.taggeditem": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "extras.webhook": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.aggregate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.asn": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.asnrange": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.fhrpgroup": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.fhrpgroupassignment": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.ipaddress": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.iprange": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.prefix": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.rir": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.role": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.routetarget": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.service": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.servicetemplate": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.vlan": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.vlangroup": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "ipam.vrf": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "tenancy.contact": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "tenancy.contactassignment": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "tenancy.contactgroup": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "tenancy.contactrole": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "tenancy.tenant": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "tenancy.tenantgroup": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "virtualization.cluster": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "virtualization.clustergroup": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "virtualization.clustertype": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "virtualization.virtualdisk": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "virtualization.virtualmachine": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "virtualization.vminterface": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "vpn.ikepolicy": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "vpn.ikeproposal": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "vpn.ipsecpolicy": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "vpn.ipsecprofile": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "vpn.ipsecproposal": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "vpn.l2vpn": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "vpn.l2vpntermination": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "vpn.tunnel": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "vpn.tunnelgroup": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "vpn.tunneltermination": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "wireless.wirelesslan": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "wireless.wirelesslangroup": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ],
    "wireless.wirelesslink": [
        "netbox_field_permissions.validators.FieldPermissionValidator"
    ]
}
```
</details>

You can also view updated configuration on the `Plugins -> Field Permissions -> Manage Validator` page.

## Features

### Disallow changes to any user accessible field

When someone tries to alter a field they don't have access to an error will be emitted.
![Example permission denied](docs/img/action_denied.png)

### Easily verify validator install
Dynamic configurations can benefit from automatic (un)install of validator for every model.
![Config validation](docs/img/validator_config.png)

## Pending features
- Better selection of fields (some of the fields are for users but are currently shown).
- Better field names that match the other NetBox forms.
