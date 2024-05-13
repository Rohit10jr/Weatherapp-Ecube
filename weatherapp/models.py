from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# current_datetime = timezone.now()
# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True, default=now)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'cities'