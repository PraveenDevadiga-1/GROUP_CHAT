from django.db import models
from django.contrib import auth
from groups.get_username import current_request
# Create your models here.
class User(auth.models.User,auth.models.PermissionsMixin):
    def __str__(self):
        return "@{}".format(self.username)
