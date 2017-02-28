from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponseBadRequest, QueryDict
from django.views.decorators.http import require_http_methods
from glgl_app.models import *

@require_http_methods(["GET"])
def search_mainpage(request):
	return render(request, "search-result.html", 
				  context = {'pattern': request.GET["title_include"], 
				  'videos': Video.objects.filter(status = 0, 
												 title__icontains = request.GET["title_include"])})

@require_http_methods(["GET"])
def search_html(request, category_id):
	return render(request, "search-result.html", 
				  context = {'pattern': request.GET["title_include"], 
				  'videos': Video.objects.filter(status = 0, category = category_id, 
												 title__icontains = request.GET["title_include"])})
