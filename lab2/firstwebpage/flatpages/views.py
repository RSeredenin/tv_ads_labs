from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'templates/index.html')


def hello(request):
    # Тип ответа не указан -> по умолчанию "text/html; charset=utf-8"
    return HttpResponse(u'Коммерческая служба телекомпании. Приём рекламы в эфир!')


def static_handler(request):
    return render(request, 'templates/static_handler.html')
