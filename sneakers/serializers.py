from authors.models import Profile
from authors.validators import AuthorsSneakerValidator
from rest_framework import serializers

from .models import Sneaker


class SneakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sneaker
        fields = [
            'author', 'id', 'title', 'description', 'price',
            'category', 'public', 'condition', 'sneaker_description',
            'condition_value', 'price_unit', 'cover'
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)
    condition = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    def get_condition(self, sneaker):
        return f'{sneaker.condition_value}{sneaker.condition_unit}'

    def validate(self, attrs):
        super_validate = super().validate(attrs)
        AuthorsSneakerValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
        )
        return super_validate

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['author', 'bio', 'contact']
