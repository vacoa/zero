from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from datetime import datetime


def home(request):
    return render(request, 'gui/home.html')

def dashboard(request):
    return render(request, 'gui/dashboard.html')

def manual(request):
    return render(request, 'gui/manual.html')

def about(request):
    return render(request, 'gui/about.html')

def react(request):
    return render(request, 'gui/react.html')

def sample(request):
    return render(request, 'gui/sample.html')

