from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Servant

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'servants/index.html'
    context_object_name = 'servants_list'

    def get_queryset(self):
        return Servant.objects.order_by('name')[:10]

class DetailView(generic.DetailView):
    model = Servant
    template_name = 'servants/detail.html'

class NPView(generic.DetailView):
    model = Servant
    template_name = 'servants/np.html'


