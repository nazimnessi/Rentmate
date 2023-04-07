from rest_framework import serializers
from .models import Room, Documents, Building


class BuildingProfilePictureSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Building
        fields = ['photo', 'name']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = '__all__'


class BuildingDocumentSerializer(serializers.Serializer):
    documents = serializers.ListField(child=serializers.FileField(), required=True)
    name = serializers.CharField()


class RoomSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class RoomDocumentSerializer(serializers.Serializer):
    documents = serializers.ListField(child=serializers.FileField(), required=True)
    name = serializers.CharField()
