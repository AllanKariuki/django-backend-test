from django.db import models
from accounts.models import CustomUser as User

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    town = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)

    def __str__(self):
        return self.first_name
