from django.contrib.auth.models import User
from rest_framework import serializers


class SneakerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published')
    condition = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    def get_condition(self, sneaker):
        return f'{sneaker.condition_value} {sneaker.condition_unit}'
