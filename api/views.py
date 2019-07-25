from django.shortcuts import HttpResponse
import json
from mockserver.loader import load_rules
from .models import Project
# Create your views here.
def test(request):

    return HttpResponse('hello world !')