from app.sites import CustomAdminsite
from django.contrib.admin import ModelAdmin, display
from django.utils.html import format_html
from app.models import CustomUser
from django.apps.registry import apps

# Register your models here.
custom_site = CustomAdminsite(name= "custom")

class ModelCustomUser(ModelAdmin):

    @display(description= "Profile Image")
    def photo_handler(self, obj= None):
        if self.profile_image:
            return format_html(f"<img src='{self.profile_image.url}' width=150 height=150>")
        else:
            return format_html(f"<p style= color:red;>Provide Image</p>")
    
    list_display = ("username", photo_handler)

custom_site.register(CustomUser, ModelCustomUser)
if apps.models_ready:
    for model in apps.get_models():
        try:
            custom_site.register(model)
        except:
            pass