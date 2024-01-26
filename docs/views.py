
import json, os, re
from os.path import join

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View


from django.templatetags.static import static        # For URL of static files
from django.conf import settings  # For load static settings

# For CSRF protection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

# Own imports
from ecuapassdocs.ecuapassutils.resourceloader import ResourceLoader 
from ecuapassdocs.ecuapassutils.pdfcreator import CreadorPDF 

def index (request):
	return (render (request, "index.html", {}))
