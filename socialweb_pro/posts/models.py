from django.db import models
from django.urls import reverse
from django.conf import settings
from groups.get_username import current_request
import misaka
from groups.models import Group
# Create your models here.

from django.contrib.auth import get_user_model
User=get_user_model()

def my_save(group):
    global var
    var=group

class Post(models.Model):
    user=models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    message=models.TextField()
    message_html=models.TextField(editable=False)
    group=models.ForeignKey(Group,related_name='posts',null=True,blank=True,on_delete=models.CASCADE)


    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        k=current_request()
        self.group=var
        self.user=k.user
        self.message_html=misaka.html(self.message)
        super(Post,self).save(*args,**kwargs)


    class Meta:
        ordering=['-created_at']
