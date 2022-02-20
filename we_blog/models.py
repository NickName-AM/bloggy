from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class OurBlog(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField(max_length=30, null=False)
    content = models.CharField(max_length=3000, null=False)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.writer)
