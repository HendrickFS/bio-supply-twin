from rest_framework import serializers
from .models import TransportBox, Sample

class TransportBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportBox
        fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'