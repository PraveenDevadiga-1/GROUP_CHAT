from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
# Create your views here.
class Homepage(TemplateView):
    template_name='index.html'

class AboutView(TemplateView):
    template_name='about.html'
    
class WelCome(TemplateView):
    template_name='welcome.html'

class Thanks(TemplateView):
    template_name='thanks.html'
