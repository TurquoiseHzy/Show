from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.handlers import *
from WeChatTicket.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET


class CustomWeChatView(WeChatView):

    lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)

    handlers = [
        BindAccountHandler,GetConferenceListHandler,GetUpcomingConferenceListHandler,GetMyConferenceListHandler,
        GetHelpHandler,SearchConferenceHandler,
    ]
    error_message_handler = ErrorHandler
    default_handler = DefaultHandler

    menu = {
        "button": [
            {
                "name": "我的账户",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "我的会议",
                        "key": "my_conf"
                    },
                    {
                        "type": "view",
                        "name": "联系我们",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "click",
                        "name": "帮助",
                        "key": "help"
                    },
                    {
                        "type": "click",
                        "name": "绑定",
                        "key": "bind_account"
                    }
                ]
            },
            {
                "name": "会议参与",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "即将进行的会议",
                        "key": "upcoming_conf"
                    },
                    {
                        "type": "click",
                        "name": "全部会议",
                        "key": "all_conf"
                    },
                    {
                        "type": "view",
                        "name": "会议签到",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "当前会议评论",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "会议搜索",
                        "url": "http://www.soso.com/"
                    }
                ]
            },
            {
                "name": "热门活动",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "活动一",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "活动二",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "活动三",
                        "url": "http://www.soso.com/"
                    }
                ]
            }
        ]
    }
    @classmethod
    def update_menu(cls, activities=None):
        """
        :param activities: list of Activity
        :return: None


        to do ...
        """