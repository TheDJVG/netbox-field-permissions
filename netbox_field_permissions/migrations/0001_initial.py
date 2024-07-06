import sys

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.core.cache import cache
from django.db import migrations, models
from django.utils.termcolors import colorize

from netbox_field_permissions.constants import (
    FIELDPERMISSION_OBJECT_TYPES,
    FIELDPERMISSION_VALIDATOR,
)


# Method to clear the config cache. To make sure NetBox will use the latest version after the migrations.
def clear_config_cache():
    cache.delete("config")
    cache.delete("config_version")


def get_current_config(apps):
    ConfigRevision = apps.get_model("core", "ConfigRevision")

    if cached_config_version := cache.get("config_version"):
        config_qs = ConfigRevision.objects.filter(pk=cached_config_version)
        return config_qs.first().data if config_qs.exists() else {}

    last_config_from_db = ConfigRevision.objects.last()

    return last_config_from_db.data if last_config_from_db else {}


def write_static_configuration_messsage():
    sys.stdout.write(
        colorize(
            "\n  Static NetBox configuration detected. Please install customer validator manually!!",
            fg="yellow",
            opts=("bold",),
        )
    )
    sys.stdout.flush()


def config_install_validator(apps, schema_editor):
    """
    Install the custom validator.
    """
    if hasattr(settings, "CUSTOM_VALIDATORS"):
        write_static_configuration_messsage()
        return

    ConfigRevision = apps.get_model("core", "ConfigRevision")
    ObjectType = apps.get_model("core", "ObjectType")

    content_types = ObjectType.objects.filter(FIELDPERMISSION_OBJECT_TYPES).order_by(
        "app_label"
    )
    install_for_content_types = [f"{ct.app_label}.{ct.model}" for ct in content_types]

    initial = get_current_config(apps)

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
        initial["CUSTOM_VALIDATORS"] = validators
        # Create a new config revision
        ConfigRevision.objects.create(
            comment="Validators added by NetBox Field Permissions plugin migration.",
            data=initial,
        )
        clear_config_cache()


# Uninstall validator
def config_uninstall_validator(apps, schema_editor):
    """
    Uninstall the custom validator.
    """
    ConfigRevision = apps.get_model("core", "ConfigRevision")

    initial = get_current_config(apps)

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
        # Create a new config revision
        ConfigRevision.objects.create(
            comment="Validators removed by NetBox Field Permissions plugin migration.",
            data=initial,
        )
        clear_config_cache()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0064_configrevision"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FieldPermission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("enabled", models.BooleanField(default=True)),
                (
                    "actions",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=30),
                        default=list,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        limit_choices_to=FIELDPERMISSION_OBJECT_TYPES,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="core.objecttype",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True, related_name="+", to="users.group"
                    ),
                ),
                (
                    "users",
                    models.ManyToManyField(
                        blank=True, related_name="+", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.RunPython(config_install_validator, config_uninstall_validator),
    ]
