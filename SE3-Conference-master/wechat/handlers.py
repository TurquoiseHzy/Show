# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
import json
import requests
import re
from wechat.models import *
from codex.baseerror import *
from WeChatTicket import settings

__author__ = "Epsirom"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')

def getConfDetailById(id):
    postUrl = 'http://60.205.137.139/adminweb/REST/API-V2/confDetail?confid=' + str(id)
    retInfo = requests.get(postUrl).json()
    if (retInfo['code'] == 0):
        return retInfo['data']
    else:
        raise ValidateError('会议详情获取失败！')


class GetHelpHandler(WeChatHandler):

    def check(self):
        return self.is_text('帮助', 'help') or self.is_event_click('help')

    def handle(self):
        return self.reply_text('初次使用时请先点击绑定')


class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_event('scan', 'subscribe')

    def handle(self):
        with open('configs.json', 'r') as f:
            data = json.load(f)
        #print(data)
        appid = data['WECHAT_APPID']
        secret = data['WECHAT_SECRET']
        openid = self.input['FromUserName']
        user = User.get_by_openid(openid)
        get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid\
                               + '&secret=' + secret
        r = requests.get(get_access_token_url)
        #print(r.json())
        access_token = r.json()['access_token']
        requestUrl = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=' + access_token\
                     + '&openid=' + openid + '&lang=zh_CN'
        userInfo = requests.get(requestUrl).json()
        userInfoUrl = 'http://60.205.137.139/adminweb/REST/API-V2/loginToChinaByWeixin?nickname=' + userInfo['nickname']\
                      + '&unionid=' + openid + '&headimgurl=' + userInfo['headimgurl'] + '&sex=' + str(userInfo['sex'])\
                      + '&location=' + userInfo['province'] + '&language=' + userInfo['language']
        retInfo = requests.post(userInfoUrl).json()
        if (retInfo['code']==0):
            user.user_id = str(retInfo['data']['id'])
            user.save()
            #return self.reply_text('绑定成功！')
        #else:
         #   return self.reply_text('绑定失败！')
def getConfList(interface, user_id, page, page_size):
    getUrl = 'http://60.205.137.139/adminweb/REST/API-V2/'+interface+'?userid=' + user_id + \
             '&page=' + str(page) + '&page_size=' + str(page_size)
    retInfo = requests.get(getUrl)
    retInfo = retInfo.json()
    news = []
    if (retInfo['code'] == 0):
        conf = retInfo['data']
        length = len(conf)
        for i in range(0, length):
            news.append({
                'Title': conf[i]['name'],
                'PicUrl': 'http://60.205.137.139/adminweb/' + conf[i]['image'],
                'Url': settings.get_url('u/conference', {'conf_id': str(conf[i]['id']), 'user_id': user_id})
            })
    return news



class GetConferenceListHandler(WeChatHandler):

    def check(self):
        return self.is_text('会议') or self.is_event_click('all_conf')

    def handle(self):
        page_size = 5
        openid = self.input['FromUserName']
        user = User.get_by_openid(openid)
        news = getConfList('allConfList', user.user_id, user.all_conf_page, page_size)
        if (news == []):
            if (user.all_conf_page == 1):
                return self.reply_text('当前没有会议。')
            else:
                user.all_conf_page = 1
                user.save()
                news = getConfList('allConfList', user.user_id, user.all_conf_page, page_size)
        news.append({
            'Title': '当前是第' + str(user.all_conf_page)
                     + '页，再次点击“全部会议”进入下一页。',
            'Url': 'about:blank',
        })
        user.all_conf_page += 1
        user.save()

        return self.reply_news(news)


class GetUpcomingConferenceListHandler(WeChatHandler):

    def check(self):
        return self.is_text('即将') or self.is_event_click('upcoming_conf')

    def handle(self):
        page_size = 5
        openid = self.input['FromUserName']
        user = User.get_by_openid(openid)
        news = getConfList('upcomingConfList', user.user_id, user.upcoming_conf_page, page_size)
        if (news == []):
            if (user.upcoming_conf_page == 1):
                return self.reply_text('当前没有即将进行的会议。')
            else:
                user.upcoming_conf_page = 1
                user.save()
                news = getConfList('upcomingConfList', user.user_id, user.upcoming_conf_page, page_size)
        news.append({
            'Title': '当前是第' + str(user.upcoming_conf_page)
                     + '页，再次点击“即将进行的会议”进入下一页。',
            'Url': 'about:blank'
        })
        user.upcoming_conf_page += 1
        user.save()
        return self.reply_news(news)


class GetMyConferenceListHandler(WeChatHandler):

    def check(self):
        return self.is_text('我的会议') or self.is_event_click('my_conf')

    def handle(self):
        page_size = 5
        openid = self.input['FromUserName']
        user = User.get_by_openid(openid)
        news = getConfList('favoriteConfList', user.user_id, user.my_conf_page, page_size)
        if (news == []):
            if (user.my_conf_page == 1):
                return self.reply_text('您还没有报名会议。')
            else:
                user.my_conf_page = 1
                user.save()
                news = getConfList('favoriteConfList', user.user_id, user.my_conf_page, page_size)
        news.append({
            'Title': '当前是第' + str(user.my_conf_page)
                     + '页，再次点击“我的会议”进入下一页。',
            'Url': 'about:blank'
        })
        user.my_conf_page += 1
        user.save()
        return self.reply_news(news)


class SearchConferenceHandler(WeChatHandler):

    def check(self):
        return self.is_msg_type('text') and re.match('^搜索 .*$', self.input['Content'])

    def handle(self):
        content = self.input['Content'][3:]
        page_size = 10
        openid = self.input['FromUserName']
        user = User.get_by_openid(openid)
        getUrl = 'http://60.205.137.139/adminweb/REST/API-V2/searchConfList?userid=' + user.user_id\
                 + '&page=1&page_size=' + str(page_size) + '&content=' + content
        retInfo = requests.get(getUrl)
        retInfo = retInfo.json()
        if (retInfo['code']==0):
            news = []
            conf = retInfo['data']
            length = len(conf)
            for i in range(0, length):
                detail = getConfDetailById(conf[i]['id'])
                news.append({
                    'Title': conf[i]['name'],
                    'PicUrl': 'http://60.205.137.139/adminweb/'+conf[i]['image'],
                    'Url': self.url_conf_detail(conf[i]['id'], user.user_id),
                })
            # 功能测试：
            # 会议列表为空的判断
            if (news == []):
                return self.reply_text('找不到和您搜索的“'+ content +'”相符的会议。')
            else:
                return self.reply_news(news)
        else:
            return self.reply_text('您的会议获取失败！')