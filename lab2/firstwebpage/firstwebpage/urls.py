from django.contrib import admin
from django.urls import path

from flatpages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('hello/', views.hello, name='hello'),
    path('static_handler/', views.static_handler, name='static_handler'),
]
