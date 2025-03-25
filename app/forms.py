from django import forms
from app.models import *
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

class ProfileForm(forms.ModelForm):

    class Meta:

        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone_number", "message", "country", "profile_image"]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control p-0 border-0",
                    "placeholder": "Johnathan"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control p-0 border-0",
                    "placeholder": "Doe"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control p-0 border-0",
                    "placeholder": "johnathan@admin.com",
                    "id": "example-email",
                    "name": "example-email"
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control p-0 border-0",
                    "placeholder": "123 456 7890"
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control p-0 border-0",
                    "rows": "5",
                }
            ),
            "country": forms.Select(
                attrs={
                    "class": "form-select shadow-none p-0 border-0 form-control-line",
                }, choices= COUNTRY
            ),
            # "profile_image": forms.ImageField(
            # )
        }

class CustomUserForm(forms.ModelForm):

    class Meta:

        model = CustomUser
        fields = ["first_name", "last_name", "username", "phone_number", "country", "message", "profile_image"]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control p-0 border-0",
                    "placeholder": "Johnathan"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control p-0 border-0",
                    "placeholder": "Doe"
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "form-control p-0 border-0",
                    "placeholder": "Doe"
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control p-0 border-0",
                    "placeholder": "123 456 7890"
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control p-0 border-0",
                    "rows": "5",
                }
            ),
            "country": forms.Select(
                attrs={
                    "class": "form-select shadow-none p-0 border-0 form-control-line",
                }, choices= COUNTRY
            ),
            # "profile_image": forms.ImageField(
            # )
        }

class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category
        fields = '__all__'

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-select shadow-none p-0 border-0 form-control-line"
                }
            )
        }

class ProductForm(forms.ModelForm):

    class Meta:

        model = Product
        fields = '__all__'

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-select shadow-none p-0 border-0 form-control-line"
                }
            ),
            "price": forms.TextInput(
                attrs={
                    "class": "form-select shadow-none p-0 border-0 form-control-line",
                    "type": "number"
                }
            ),
            
        }
        
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        if isinstance(widget:=self.fields["category"].widget, RelatedFieldWidgetWrapper):
            
            widget.attrs["class"] = "form-select shadow-none p-0 border-0 form-control-line"

