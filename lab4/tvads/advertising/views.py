from django.http import Http404
from django.shortcuts import render

from .models import Advertisement


def archive(request):
    return render(request, 'archive.html',
                  {"posts": Advertisement.objects.all()})


def get_ad(request, ad_id):
    try:
        post = Advertisement.objects.get(id=ad_id)
        return render(request, 'ad.html', {"post": post})
    except Advertisement.DoesNotExist:
        raise Http404
