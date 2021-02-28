from django.shortcuts import render, redirect
#own
from django.conf import settings
import neuralStyleProcess
from django.urls import reverse

import cv2

# Create your views here.
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    )
from .models import Arts
from .forms import ArtsForm
# Create your views here.


class ArtsListView(ListView):
    model = Arts
    template_name = "arts/home.html"
    context_object_name = 'arts'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super(ArtsListView, self).get_context_data(**kwargs)
        context.update({
            'arts': Arts.objects.all().order_by('?'),
            'arts_udnie': Arts.objects.filter(action='UDNIE').order_by('-date'),
            'arts_candy': Arts.objects.filter(action='CANDY').order_by('-date'),
            'arts_mosaic': Arts.objects.filter(action='MOSAIC').order_by('-date'),
            'arts_pink': Arts.objects.filter(action='PINK').order_by('-date'),
            'arts_scream': Arts.objects.filter(action='SCREAM').order_by('-date'),
            'arts_lamuse': Arts.objects.filter(action='LA_MUSE').order_by('-date'),
            'arts_fire': Arts.objects.filter(action='FIRE').order_by('-date'),
            'arts_flame': Arts.objects.filter(action='FLAME').order_by('-date'),
            'arts_rain': Arts.objects.filter(action='RAIN').order_by('-date'),
            'arts_landscape': Arts.objects.filter(action='LANDSCAPE').order_by('-date'),
            'arts_goldblack': Arts.objects.filter(action='GOLD_BLACK').order_by('-date'),
            'arts_triangle': Arts.objects.filter(action='TRIANGLE').order_by('-date'),
            'arts_starrynight': Arts.objects.filter(action='STARRY_NIGHT').order_by('-date'),
            'arts_wave': Arts.objects.filter(action='WAVE').order_by('-date'),
            'arts_feathers': Arts.objects.filter(action='FEATHERS').order_by('-date'),
        })
        return context



class ArtsDetailView(DetailView):
    model = Arts
    template_name = "arts/art_detail.html"


class ArtsCreateView(CreateView):
    template_name = 'arts/art_form.html'
    form_class = ArtsForm

    def upload(self, request):
        form = ArtsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return render(request, self.template_name, {'form':form},)
        

class CategoryView(ListView):
    model = Arts
    template_name = 'arts/art_category.html'
    context_object_name = 'arts'

    def get_queryset(self):
        # action = Arts.objects.get(action=self.kwargs['action'][0])
        queryset = Arts.objects.order_by('-id').filter(action=self.kwargs['action'])
        return queryset

    #アクセスした値を取得し辞書に格納
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_key'] = self.kwargs['action']
        return context