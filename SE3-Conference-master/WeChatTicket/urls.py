"""WeChatTicket URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

from wechat.views import *
from WeChatTicket.views import *


urlpatterns = [
    url(r'^wechat/?$', CustomWeChatView.as_view()),
    url(r'^wechat/api/conf?$', APIConf.as_view()),
    url(r'^wechat/api/login?$', AdminLogin.as_view()),
    url(r'^wechat/api/conferenceList?$', ConferenceList.as_view()),
    url(r'^wechat/api/price?$', ChangePrice.as_view()),
    url(r'^wechat/api/getConfPrice?$', GetConfPrice.as_view()),
    url(r'^wechat/api/joinConf?$', JoinConf.as_view()),
    url(r'^wechat/api/quitConf?$', QuitConf.as_view()),
    url(r'^wechat/api/remind?$', Remind.as_view()),
    url(r'^', StaticFileView.as_view()),
]
