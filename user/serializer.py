from rest_framework import serializers
from .models import User, Documents


class UserProfilePictureSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = User
        fields = ['photo', 'name']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserDocumentSerializer(serializers.Serializer):
    documents = serializers.ListField(child=serializers.FileField(), required=True)
    name = serializers.CharField()
