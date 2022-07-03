from django.db import models

# Create your models here.

class Registration(models.Model):
    frist_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=40)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + self.last_name