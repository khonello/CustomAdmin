from typing import Any, Dict, Optional, Type
from django import http
from django.contrib.admin import AdminSite
from django.contrib.admin.views.main import ChangeList
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from app.models import *
from django.db.models.query import Q, QuerySet
from app.forms import *
from django.urls import path
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps.registry import apps
from itertools import dropwhile
from django.contrib.admin import ModelAdmin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


developers, _ = Group.objects.get_or_create(name= "Developers")
administrators, _ = Group.objects.get_or_create(name= "Administrators")

user_contenttype = ContentType.objects.get_for_model(CustomUser)

update_permission, _ = Permission.objects.get_or_create(codename= "update_website", name= "can update website", content_type= user_contenttype)
shutdown_permission, _ = Permission.objects.get_or_create(codename= "shutdown_website", name= "can shutdown website", content_type= user_contenttype)

developers.permissions.add(update_permission, shutdown_permission)

class DashboardView(TemplateView):

    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs: Any):

        context_data = {
            "sales": Sale.objects.all().order_by("-date_added"),
            "comments": Comment.objects.all().filter(Q(status__contains= "approved") | Q(status__contains= "pending")).order_by("-date_added"),
            "staffs": CustomUser.objects.filter(is_staff= True),
            "products": Product.objects.all().order_by("id"),
            "categories": Category.objects.all().order_by("id"),
        }

        return context_data
    
    def dispatch(self, request, *args: Any, **kwargs: Any):

        return super().dispatch(request, *args, **kwargs)
    
class ProfileView(UpdateView):

    template_name = "profile/profile.html"
    form_class = ProfileForm
    context_object_name = "custom_user_obj"
    pk_url_kwarg = "pk"
    success_url = "/admin/"
    
    def get_queryset(self):

        return CustomUser.objects.all()
    
    def dispatch(self, request, *args: Any, **kwargs: Any):

        return super().dispatch(request, *args, **kwargs)

class UsersView(TemplateView):
    
    template_name = "users/users.html"
    
    def get_context_data(self, **kwargs: Any):

        adminstrators = Group.objects.get(name= "Administrators").customuser_set.all()
        # developers = CustomUser.objects.filter(user_permissions__codename= "")
        developers = Group.objects.get(name= "Developers").customuser_set.all()
        customers = CustomUser.objects.filter(Q(is_superuser= False) | Q(is_staff= False)).order_by('-id')

        context_data = {
            "administrators": adminstrators,
            "developers": developers,
            "customers": customers
        }
        return context_data
    
    def dispatch(self, request, *args: Any, **kwargs: Any):

        return super().dispatch(request, *args, **kwargs)
    
class TablesView(TemplateView):

    template_name = "tables/tables.html"

    def get_context_data(self, **kwargs: Any):

        context_data = {}
        registered_models = apps.get_models()

        for app in apps.get_app_configs():

            app_label = app.label
            context_data[app_label] = {}

            for key, value in app.models.items():

                context_data[app_label][key] = []
                for model in registered_models:

                    if model == value:
                        context_data[app_label][key] += [[value.__name__, value]]


        def del_apps(*args, **kwargs):
            '''
            Delete apps that don't hold any values
            '''
            to_delete_app = []

            for app in context_data:
                if not context_data[app]:

                    to_delete_app.append(app)

            for _app in to_delete_app:

                del context_data[_app]

        def del_models(*args, **kwargs):
            
            '''
            Delete app keys that don't hold any values
            '''
            to_delete = []

            for app in context_data:
                for model_key in context_data[app]:
                    if not context_data[app][model_key]:

                        to_delete.append([app, model_key])

            for _app, _key  in to_delete:
                del context_data[_app][_key]

        del_apps()
        del_models()

        context = {
            "apps_config": context_data
        }
        
        return context
    
    def dispatch(self, request, *args: Any, **kwargs: Any):

        return super().dispatch(request, *args, **kwargs)

class CustomAdminsite(AdminSite):

    site_header = "Site Header"
    site_title = "Administration"

    def register_model(self, *args, **kwargs):
    
        context = TablesView.get_context_data(TablesView)

        for _, important in context.items():

            for app, model_items in important.items():
                
                for model_name, model_class in model_items.items():
                    
                    ModelAdminClass = f"Model{model_name.title()}"
                    ChangeListClass = f"ChangeList{model_name.title()}"

                    class ChangeListClass(ChangeList):
                         
                        def get_queryset(self, request: WSGIRequest):

                            queryset = self.model.objects.all()
                            return queryset
                
                    class ModelAdminClass(ModelAdmin):
                    
                        change_list_template = "changelist/changelist.html"
                        change_form_template = "changeform/changeform.html"
                        delete_confirmation_template = "confirm_delete/confirm_delete.html"
                                    
                        # class Media:
                            
                            # css = {
                            #     "all": (r"css\style.min.css",)
                            # }

                            # js = ("script.js",)

                        @classmethod
                        def custom_user(cls, form= None, user_model= False):
                            
                            if user_model:
                                cls.fieldsets = [
                                    ("Personal Info",    {
                                        "fields": ["first_name", "last_name", "username"],
                                        "description": "Description",
                                        "classes": ["col-md-12 border-bottom p-0"]
                                        }
                                    ),
                                    ("Other Details",    {
                                        "fields": ["phone_number", "country", "message", "profile_image"],
                                        "description": "Description",
                                        "classes": ["col-md-12 border-bottom p-0"]
                                        }
                                    )
                                ]

                            cls.readonly_fields = []
                            if form:
                                cls.form = form


                        def get_changelist(self, request: HttpRequest, **kwargs: Any):
                            
                            return ChangeListClass
                        
                        def changelist_view(self, request: HttpRequest, extra_context= None):

                            changelist_queryset = self.get_queryset(request).order_by("id")
                            changelist_paginator = self.get_paginator(request, changelist_queryset, 10)
                            changelist_instance = self.get_changelist_instance(request) 

                            page_num = request.GET.get("page")

                            try:

                                paginator_queryset = changelist_paginator.page(page_num)
                            except PageNotAnInteger:

                                paginator_queryset = changelist_paginator.page(1)
                            except EmptyPage:

                                paginator_queryset = changelist_paginator.page(changelist_paginator.num_pages)

                            model = changelist_instance.model
                            model_admin: ModelAdminClass = changelist_instance.model_admin

                            # changelist_instance_options = changelist_instance.opts
                            extra_extra_context = {
                                "objects": paginator_queryset,
                            }

                            # changelist_view_data = super().changelist_view(request, extra_context= extra_context)
                            # changelist_context = changelist_view_data.context_data["cl"]

                            return super().changelist_view(request, extra_context= extra_extra_context)
                    
                        def changeform_view(self, request: HttpRequest, object_id, form_url, extra_context= None):
                            
                            match (self.opts.model_name):
                                case "customuser":
                                    self.custom_user(form= CustomUserForm, user_model= True)
                                case "category":
                                    self.custom_user(form= CategoryForm)
                                case "product":
                                    self.custom_user(form= ProductForm)


                            return super().changeform_view(request, object_id, form_url, extra_context)
                        
                        # def add_view(self, request: HttpRequest, form_url, extra_context= None):

                        #     return super().add_view(request, form_url, extra_context)

                    self.unregister(model_class[0][1])

                    try:
                        self.register(model_class[0][1], ModelAdminClass)
                    except:
                        self.register(model_class[0][1])
                                       
    def get_urls(self):

        self.register_model()

        first_urls =  super().get_urls()
        second_urls = [
            path("", self.admin_view(self.dashboard_view), name= "dashboard"),
            path("profile/<int:pk>/", self.admin_view(self.profile_view), name= "profile"),
            path("users/", self.admin_view(self.users_view), name= "users"),
        ]

        return second_urls + first_urls
    

    def app_index(self, request: WSGIRequest, app_label: str, extra_context= None):
        # This method handles listing of the models in all the apps

        return TablesView.as_view()(request)
    
    def dashboard_view(self, request):

        return DashboardView.as_view()(request)
    
    def profile_view(self, request, *args, **kwargs):

        return ProfileView.as_view()(request, pk= kwargs['pk'])

    def users_view(self, request, *args, **kwargs):

        return UsersView.as_view()(request)
 