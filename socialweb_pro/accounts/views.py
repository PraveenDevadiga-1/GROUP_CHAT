from django.shortcuts import render
from django.views.generic import TemplateView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
# Create your views here.

class Signup (CreateView):
    form_class=forms.UserCreateForm
    success_url=reverse_lazy('login')
    template_name='accounts/signup.html'
