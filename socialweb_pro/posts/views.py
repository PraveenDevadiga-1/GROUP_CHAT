from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.contrib import messages
from groups.models import Group,GroupMember
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your views here.
class PostList(SelectRelatedMixin,generic.ListView):
    model=models.Post
    select_related=('user','group')


class PostDetail(SelectRelatedMixin,generic.DetailView):
    model=models.Post
    select_related=('user','group')

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))



class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model=models.Post
    select_related=('user','group')

    def get_success_url(self):
        return reverse_lazy('groups:single', kwargs={'slug': self.object.group.slug})

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)

class UserPosts(generic.ListView):
    model = GroupMember
    template_name = "posts/user_post_list.html"
    context_object_name = 'user_groups'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.memberships.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context
