from django.shortcuts import render
from rest_framework import viewsets
from .models import TransportBox, Sample
from .serializers import TransportBoxSerializer, SampleSerializer


class TransportBoxViewSet(viewsets.ModelViewSet):
    queryset = TransportBox.objects.all()
    serializer_class = TransportBoxSerializer
    lookup_field = 'box_id'

class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    lookup_field = 'sample_id'