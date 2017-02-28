"""glgl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from glgl_app import views as glgl_app_views
from glgl_app import models as glgl_app_models
from glgl_app import video as glgl_app_video
from glgl_app import search as glgl_app_search
import glgl.settings as settings
urlpatterns = [
	url(r'^$', glgl_app_views.index),
	url(r'^about/',glgl_app_views.aboutus),
	url(r'^category/(?P<category_id>[0-9]+)', glgl_app_views.category),
	url(r'^login/',glgl_app_models.login),
	url(r'^logout/',glgl_app_models.logout),
	url(r'^register/',glgl_app_models.register),
	url(r'^home/',glgl_app_views.home),
	url(r'^profile/',glgl_app_models.profile),
	url(r'^homepage/(?P<user_id>[0-9]+)/', include([
		url(r'^$', glgl_app_views.homepage)
	])),
	url(r'^setpassword/',glgl_app_models.setPassword),
	url(r'^setpassword-suc/',glgl_app_views.setPasswordSuc),
	url(r'^upload/$', glgl_app_models.upload),
	url(r'^video/(?P<video_id>[0-9]+)/', include([
		url(r'^$', glgl_app_video.video_play),
		url(r'^passvideo/$', glgl_app_video.video_pass),
		url(r'^banvideo/$', glgl_app_video.video_ban),
		url(r'^likethis/$', glgl_app_video.like)
	])),
	url(r'(?P<video_id>[0-9]+)/morecomments/$',glgl_app_views.more_comments),
	url(r'^send-comment/$',glgl_app_video.video_comment_add),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	url(r'^search/',include([
		url(r'^$',glgl_app_search.search_mainpage),
		url(r'^(?P<category_id>[0-9]+)/', glgl_app_search.search_html)
	])),
	url(r'^admin/', admin.site.urls),
	url(r'^check/', glgl_app_views.checkpage),
	url(r'^banvideo/', glgl_app_views.banpage)
]
