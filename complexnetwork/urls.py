from django.conf.urls import url
from . import views

app_name = 'complexnetwork'
urlpatterns = [
    url(r'^$', views.chineseNetwork2, name='index'),
]
