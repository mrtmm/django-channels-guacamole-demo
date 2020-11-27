from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("HELLO!")


def ws(request):
    return render(request, 'index.html', {})
