import itertools
import logging
from collections import defaultdict

from core.models import ConfigRevision, ObjectType
from django.db import models
from netbox.config import get_config

from netbox_field_permissions.constants import (
    FIELDPERMISSION_OBJECT_TYPES,
    FIELDPERMISSION_VALIDATOR,
)
from netbox_field_permissions.models import FieldPermission

logger = logging.getLogger(__name__)


def get_disabled_fields(user, model, action):
    content_type = ObjectType.objects.get_for_model(model)

    fields = FieldPermission.objects.filter(
        models.Q(users=user) | models.Q(groups__user=user),
        enabled=True,
        content_type=content_type,
    ).values_list("actions", flat=True)
    fields = set(itertools.chain(*fields))

    disabled_fields = []
    for field in fields:
        name, disabled_action = field.split(":")
        if disabled_action == action:
            disabled_fields.append(name)

    return disabled_fields


def validator_status_by_content_type():
    content_types = ObjectType.objects.filter(FIELDPERMISSION_OBJECT_TYPES).order_by(
        "app_label"
    )

    # Use the active config so no database has to be hit.
    config = get_config().config.get("CUSTOM_VALIDATORS", {})

    data = defaultdict(list)

    for ct in content_types:
        app_label = ct.app_label
        model = ct.model
        lookup = f"{app_label}.{model}"

        data[app_label].append(
            {
                "model": model,
                "enabled": FIELDPERMISSION_VALIDATOR in config.get(lookup, {}),
            }
        )

    return data


# Sorry Jeremy, I'm sure you're not going to like the following.
def install_validator():
    content_types = ObjectType.objects.filter(FIELDPERMISSION_OBJECT_TYPES).order_by(
        "app_label"
    )
    install_for_content_types = [f"{ct.app_label}.{ct.model}" for ct in content_types]

    config_version = get_config().version
    config_qs = ConfigRevision.objects.filter(pk=config_version)

    initial = config_qs.first().data if config_qs.exists() else {}

    validators = initial.get("CUSTOM_VALIDATORS", {}).copy()
    needs_update = False

    for ct in install_for_content_types:
        if ct not in validators:
            needs_update = True
            validators[ct] = (FIELDPERMISSION_VALIDATOR,)
        else:
            if FIELDPERMISSION_VALIDATOR not in validators[ct]:
                needs_update = True
                validators[ct] = tuple(validators[ct]) + (FIELDPERMISSION_VALIDATOR,)

    # Check if we need to update the config
    if needs_update:
        initial["CUSTOM_VALIDATORS"] = (
            validators  # Just to be sure in case "CUSTOM_VALIDATORS" did not exist.
        )
        logger.info(
            "NetBox configuration will be updated to include Field Permission validators."
        )
        # Create a new config revision
        revision = ConfigRevision.objects.create(
            comment="Validators added by NetBox Field Permissions plugin.", data=initial
        )
        # Activate the new config.
        revision.activate()


def uninstall_validator():
    config_version = get_config().version
    config_qs = ConfigRevision.objects.filter(pk=config_version)

    initial = config_qs.first().data if config_qs.exists() else {}

    validators = initial.get("CUSTOM_VALIDATORS", {})

    needs_update = False
    for model, validator in validators.copy().items():
        if FIELDPERMISSION_VALIDATOR not in validator:
            continue

        needs_update = True
        # If there's only 1 validator defined just remove the key from the config so we don't end up with empty values.
        if len(validator) == 1:
            del validators[model]
        else:
            validator[model] = (x for x in validator if x != FIELDPERMISSION_VALIDATOR)

    if needs_update:
        initial["CUSTOM_VALIDATORS"] = (
            validators  # Just to be sure in case "CUSTOM_VALIDATORS" did not exist.
        )
        logger.info(
            "NetBox configuration will be updated to exclude Field Permission validators."
        )
        # Create a new config revision
        revision = ConfigRevision.objects.create(
            comment="Validators removed by NetBox Field Permissions plugin.",
            data=initial,
        )
        # Activate the new config.
        revision.activate()
