from django.db import models
from django.contrib.auth import get_user_model

from rest_framework_api_key.models import AbstractAPIKey, APIKey

User = get_user_model()


class Application(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    name = models.CharField(max_length=250)

    def extend_with_key(self, key):
        self.generated_key = key
        return self

    def generate_api_key(self):
        ApplicationApiKey.objects.filter(application=self).delete()
        return ApplicationApiKey.objects.create_key(name=self.name, application=self)


class ApplicationApiKey(AbstractAPIKey):
    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="api_key",
    )
