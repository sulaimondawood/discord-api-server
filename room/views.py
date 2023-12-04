from django.shortcuts import render
from django.http import HttpResponse

def room(request):
  return HttpResponse("Room")