from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Conversion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    search_text = models.CharField(max_length=5000, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.search_text
