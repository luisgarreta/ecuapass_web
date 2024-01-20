
import json, os, re
from os.path import join

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.templatetags.static import static        # For URL of static files
from django.conf import settings  # For load static settings

#
# Create your views here.
#
def index (request):
	return (render (request, "ecuapass_web/index.html", {}))
	
