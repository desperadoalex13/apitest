from rest_framework_api_key.permissions import BaseHasAPIKey

from applications.models import ApplicationApiKey


class HasApplicationAPIKey(BaseHasAPIKey):
    model = ApplicationApiKey