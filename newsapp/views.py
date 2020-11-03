from django.shortcuts import render
from .models import News
from django.views.generic import CreateView
from django.urls import reverse_lazy
import urllib.request
import requests
from bs4 import BeautifulSoup

# Create your views here.

class Create(CreateView):
   template_name = 'home.html'
   model = News
   fields = ('url',)
   success_url = reverse_lazy('list')


def listfunc(request):
   for post in News.objects.all():
       url = post.url
   list = []
   response = requests.get(url)
   bs = BeautifulSoup(response.text, "html.parser")
   ul_tag = bs.find_all(class_="topicsList_main")
   for tag in ul_tag[0]:
      title = tag.a.getText()
      url2 = tag.a.get("href")
      list.append([title, url2])
   context = {'list': list,}
   return render(request, 'list.html', context)
