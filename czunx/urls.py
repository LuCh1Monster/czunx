from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from complexnetwork import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('complexnetwork/', include('complexnetwork.urls', namespace='complexnetwork')),
]
