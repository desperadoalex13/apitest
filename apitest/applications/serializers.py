from rest_framework import serializers

from applications.models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ('id', 'name')

    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        app_instance = super().create(validated_data)
        _, created_key = app_instance.generate_api_key()
        app_instance.extend_with_key(created_key)
        return app_instance

    def to_representation(self, instance):
        data = super(ApplicationSerializer, self).to_representation(instance)
        if hasattr(instance, 'generated_key'):
            data.update({'api_key': instance.generated_key})
        return data
