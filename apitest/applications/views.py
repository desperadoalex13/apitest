from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.permissions import HasApplicationAPIKey
from applications.serializers import ApplicationSerializer
from applications.models import Application, ApplicationApiKey


class ApplicationViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'test':
            permission_classes = [HasApplicationAPIKey]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Returns queryset of objects assigned to current user.
        """
        if self.request.user.is_authenticated:
            return Application.objects.filter(user=self.request.user)
        return Application.objects.all()

    def get_serializer_context(self):
        """Extend current serializer context."""
        context = super().get_serializer_context()
        if self.action != 'test':
            context.update({'user': self.request.user})
        return context

    @action(detail=True, methods=['post'])
    def regenerate_token(self, request, pk=None):
        try:
            application = Application.objects.get(id=pk)
            _, created_key = application.generate_api_key()
            application.extend_with_key(created_key)
        except Application.DoesNotExist:
            return Response({"errors": ["Application not found"]}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def test(self, request, pk=None):
        api_key_prefix = self.get_permissions()[0].get_key(request).split('.')[0]
        app_key_obj = ApplicationApiKey.objects.get(prefix=api_key_prefix)
        serializer = self.get_serializer(app_key_obj.application)
        return Response(serializer.data, status=status.HTTP_200_OK)