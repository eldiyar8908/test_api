from django.db import models

# Create your models here.
from random import choice, randint
from django.db import models
from django.contrib.auth.models import User

class Confirm(models.Model):
    confirm_code = models.CharField(max_length=10, null=True, default=99)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=100, null=True)
    def __str__(self):
        return self.confirm_code, self.user.username