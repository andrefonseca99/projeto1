from authors.models import Profile
from rest_framework import serializers

from .models import Sneaker


class SneakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sneaker
        fields = [
            'author', 'id', 'title', 'description',
            'category', 'public', 'condition'
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)
    condition = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    def get_condition(self, sneaker):
        return f'{sneaker.condition_value} {sneaker.condition_unit}'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['author', 'bio', 'contact']
