from django.db import models

# Create your models here.

class TransportBox(models.Model):
    box_id = models.CharField(max_length=100, unique=True)
    geolocation = models.CharField(max_length=255)
    temperature = models.FloatField()
    humidity = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Box {self.box_id} - Geolocation: {self.geolocation}"
    
class Sample(models.Model):
    sample_id = models.CharField(max_length=100, unique=True)
    box = models.ForeignKey(TransportBox, related_name='samples', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    collected_at = models.DateTimeField()
    status = models.CharField(max_length=50)
    temperature = models.FloatField()
    humidity = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)
    
