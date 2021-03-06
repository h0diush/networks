from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from main.models import Group, Post, User


class GroupSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        allow_blank=False, validators=[
            UniqueValidator(
                queryset=Group.objects.all())])

    class Meta:
        model = Group
        fields = ['title', 'slug']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        slug_field='slug', queryset=Group.objects.all())

    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")
