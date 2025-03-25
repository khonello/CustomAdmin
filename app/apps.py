from django.apps import AppConfig
from django.contrib.admin.apps import SimpleAdminConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

class CustomAdminConfig(SimpleAdminConfig):

    default_site = "app.sites.CustomAdminSite"
    # label = "custom_admin"