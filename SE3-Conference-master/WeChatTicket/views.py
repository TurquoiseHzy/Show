# -*- coding: utf-8 -*-
#
from codex.baseview import BaseView,APIView
from WeChatTicket import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
import requests
from codex.baseerror import *
from wechat.models import *
import logging
import mimetypes
import os
import json


__author__ = "Epsirom"


class StaticFileView(BaseView):

    logger = logging.getLogger('Static')

    def get_file(self, fpath):
        if os.path.isfile(fpath):
            return open(fpath, 'rb').read()
        else:
            return None

    def do_dispatch(self, *args, **kwargs):
        if not settings.DEBUG:
            self.logger.warn('Please use nginx/apache to serve static files in production!')
            raise Http404()
        rpath = self.request.path.replace('..', '.').strip('/')
        if '__' in rpath:
            raise Http404('Could not access private static file: ' + self.request.path)
        content = self.get_file(os.path.join(settings.STATIC_ROOT, rpath))
        if content is not None:
            return HttpResponse(content, content_type=mimetypes.guess_type(rpath)[0])
        # content = self.get_file(os.path.join(settings.STATIC_ROOT, rpath + '.html'))
        # if content is not None:
        #     return HttpResponse(content, content_type=mimetypes.guess_type(rpath + '.html')[0])
        content = self.get_file(os.path.join(settings.STATIC_ROOT, rpath + '/index.html'))
        if content is not None:
            return HttpResponse(content, content_type=mimetypes.guess_type(rpath + '/index.html')[0])
        raise Http404('Could not found static file: ' + self.request.path)


class APIConf(APIView):

    def getConfInfoById(self, conf_id):
        postUrl = 'http://60.205.137.139/adminweb/REST/API-V2/confInfo?confid=' + str(conf_id)
        retInfo = requests.get(postUrl).json()
        if (retInfo['code'] == 0):
            return retInfo['data']
        else:
            raise ValidateError('会议详情获取失败！')

    def get(self):
        conf_id = self.input['conf_id']
        user_id = self.input['user_id']
        followed = checkFollower(conf_id,user_id)
        conf_info = self.getConfInfoById(conf_id)
        context = { 'conf_id': conf_id,
                    'name': conf_info['basic']['name'],
                    'image': 'http://60.205.137.139/adminweb/' + conf_info['basic']['image'],
                    'start_date': conf_info['basic']['start_date'],
                    'end_date': conf_info['basic']['end_date'],
                    'location': conf_info['basic']['location'],
                    'isPrivate': conf_info['basic']['isPrivate'],
                    'privateType': conf_info['basic']['privateType'],
                    'desc': conf_info['detail']['desc'],
                    'followed' : followed,}
        return context


class AdminLogin(APIView):

    #检查是否已登录
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError('你尚未登录！')

    #给定username和password，登录
    def post(self):
        self.check_input('username', 'password')
        try:
            user = authenticate(username=self.input['username'], password=self.input['password'])
            if user is not None:
                login(self.request, user)
            else:
                raise ValidateError('用户名或密码错误！')
        except:
            raise ValidateError('登录出现错误！')


class ConferenceList(APIView):
    def getConfDetailById(self, id):
        postUrl = 'http://60.205.137.139/adminweb/REST/API-V2/confDetail?confid=' + str(id)
        retInfo = requests.get(postUrl).json()
        if (retInfo['code'] == 0):
            return retInfo['data']
        else:
            raise ValidateError('会议详情获取失败！')

    def get(self):
        page_size = 100
        getUrl = 'http://60.205.137.139/adminweb/REST/API-V2/allConfList?userid=' + '1' + \
                 '&page=' + '1' + '&page_size=' + str(page_size)
        retInfo = requests.get(getUrl)
        retInfo = retInfo.json()
        news = []
        print(retInfo)
        if (retInfo['code']==0):
            confs = retInfo['data']
            length = len(confs)
            for i in range(0, length):
                detail = {'conf_name':'', 'price':0}
                conf = Conference.objects.filter(conf_id=confs[i]['id'])
                if len(conf) != 0:
                    detail['conf_name'] = conf[0].conf_name
                    detail['price'] = conf[0].price
                    detail['conf_id'] = conf[0].conf_id
                else:
                    conf = self.getConfDetailById(confs[i]['id'])
                    detail['conf_name'] = confs[i]['name']
                    detail['price'] = 0
                    detail['conf_id'] = confs[i]['id']
                    new_conf = Conference(conf_id=confs[i]['id'], conf_name=confs[i]['name'],price = 0)
                    new_conf.save()
                news.append(detail)
        return news


class ChangePrice(APIView):
    def post(self):
        conf = Conference.objects.filter(conf_id=self.input['conf_id'])[0]
        conf.price = self.input['price']
        conf.save()

class GetConfPrice(APIView):
    def get(self):
        conf = Conference.objects.filter(conf_id=self.input['conf_id'])[0]
        detail = {
            'price':conf.price,
            'conf_name':conf.conf_name,
        }
        return detail

class JoinConf(APIView):
    def post(self):
        status = False
        getUrl = "http://60.205.137.139/adminweb/REST/API-V2/joinConf?userid=" + self.input['user_id'] \
                 + "&confid=" + self.input['conf_id']
        retInfo = requests.post(getUrl)
        retInfo = retInfo.json()
        if retInfo['code'] == 0:
            status = True
        else:
            status = False
        return status

class QuitConf(APIView):
    def post(self):
        status = False
        getUrl = "http://60.205.137.139/adminweb/REST/API-V2/cancelConf?userid=" + self.input['user_id'] \
                 + "&confid=" + self.input['conf_id']
        retInfo = requests.post(getUrl)
        retInfo = retInfo.json()
        if retInfo['code'] == 0:
            status = True
        else:
            status = False
        return status


def checkFollower(conf_id, user_id):
    page_size = 100
    getUrl = 'http://60.205.137.139/adminweb/REST/API-V2/favoriteConfList?userid=' + user_id \
             + '&page=1&page_size=' + str(page_size)
    retInfo = requests.get(getUrl)
    retInfo = retInfo.json()
    conf = retInfo['data']
    length = len(conf)
    for i in range(0, length):
        if str(conf[i]['id']) == conf_id:
            return True
    return False

class Remind(APIView):
    def get(self):
        conf_id = self.input['conf_id']
        with open('configs.json', 'r') as f:
            data = json.load(f)
        appid = data['WECHAT_APPID']
        secret = data['WECHAT_SECRET']
        get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid \
                               + '&secret=' + secret
        r = requests.get(get_access_token_url)
        print (r.text)
        access_token = r.json()['access_token']
        requestUrl = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token
        template_id = "v7_-4_4is1o6UdwEJtko_UXPuA-4P_AA42epeF-QcZw"
        for user in User.objects.all():
            if (user.user_id == ""):
                continue
            if checkFollower(conf_id, user.user_id):
                moreinfourl = settings.get_url('u/conference', {'conf_id': str(conf_id), 'user_id': user.user_id})
                postUrl = 'http://60.205.137.139/adminweb/REST/API-V2/confInfo?confid=' + str(conf_id)
                retInfo = requests.get(postUrl).json()
                message = '{"touser":"%(open_id)s","template_id":"%(template_id)s","url":"%(url)s","data":{"conference":{"value":"%(conf_name)s","color":"#173177"}}}' \
                          % {"open_id": user.open_id, "template_id": template_id, "url": moreinfourl, "conf_name" : retInfo['data']['basic']['name']}
                message = message.encode('utf-8')
                requests.post(requestUrl, data=message).json()