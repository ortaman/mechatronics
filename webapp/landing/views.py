
from django.shortcuts import render


def index(request):
    return render(request, 'landing/index.html', context={})


def big_picture(request):
    return render(request, 'landing/big-picture.html', context={})
