from django.shortcuts import render

from .models import Advertisement


def archive(request):
    return render(request, 'archive.html',
                  {"posts": Advertisement.objects.all()})
