from django.contrib import admin
from django.urls import path

from advertising import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.archive, name='archive'),
]
