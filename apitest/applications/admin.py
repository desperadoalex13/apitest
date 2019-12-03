from django.contrib import admin

from applications.models import Application, ApplicationApiKey
from rest_framework_api_key.admin import APIKeyModelAdmin


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(ApplicationApiKey)
class ApplicationApiKeyAdmin(APIKeyModelAdmin):
    pass