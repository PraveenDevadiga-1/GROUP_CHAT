from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from braces.views import SelectRelatedMixin
from django.urls import reverse,reverse_lazy
from . import models
from django.views import generic
from groups.models import Group,GroupMember
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from posts.models import Post
from posts.forms import PostForm
from posts.models import my_save
from groups.get_username import current_request
import misaka
User=get_user_model()
# Create your views here.
class CreateGroup(LoginRequiredMixin,generic.CreateView):
     fields= ('name','description')
     model=Group

class DeleteGroup(LoginRequiredMixin,generic.DeleteView):
    model=Group
    success_url=reverse_lazy('groups:all')

class ListGroups(generic.ListView):
    model=Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,'Already a member')
        else:
            messages.success(self.request,'You are now a member')

        return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):

        try:
            membership= models.GroupMember.objects.filter(
            user=self.request.user,
            group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this group')

        else:
            membership.delete()
            messages.success(self.request,'You have left the group')
        return super().get(request,*args,**kwargs)

def GroupDetail(request,slug):
        group=Group.objects.filter(slug=slug)
        if request.method=='POST':
            post_form=PostForm(data=request.POST)
            if post_form.is_valid():
                my_save(group[0])
                post_form.save()
                return HttpResponseRedirect(reverse('groups:single',kwargs={'slug':slug}))
            else:
                print(post_form.errors)
        else:
            post_form=PostForm()
        return  render(request,'groups/group_detail.html',{'post_form':post_form,'group':group[0]})
