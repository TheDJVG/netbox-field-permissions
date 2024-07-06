from django.urls import path

from netbox_field_permissions import views

urlpatterns = [
    path(
        "field-permissions/",
        views.FieldPermissionListView.as_view(),
        name="fieldpermission_list",
    ),
    path(
        "field-permissions/add/",
        views.FieldPermissionEditView.as_view(),
        name="fieldpermission_add",
    ),
    path(
        "field-permissions/manage/",
        views.FieldPermissionManageView.as_view(),
        name="fieldpermission_manage",
    ),
    path(
        "field-permissions/<int:pk>/",
        views.FieldPermissionView.as_view(),
        name="fieldpermission",
    ),
    path(
        "field-permissions/<int:pk>/edit/",
        views.FieldPermissionEditView.as_view(),
        name="fieldpermission_edit",
    ),
    path(
        "field-permissions/<int:pk>/delete/",
        views.FieldPermissionDeleteView.as_view(),
        name="fieldpermission_delete",
    ),
]
