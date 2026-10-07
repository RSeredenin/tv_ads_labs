from django.contrib import admin
from django.urls import path, re_path

from advertising import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.archive, name='archive'),
    path('ad/new/', views.create_ad, name='create_ad'),
    re_path(r'^ad/(?P<ad_id>\d+)/$', views.get_ad, name='get_ad'),
]
