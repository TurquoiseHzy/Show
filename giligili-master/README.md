#GiliGili维护文档
[TOC]

## 文档

- 编写目的:本文档旨在说明网站代码的架构结构和功能分块。面向后续开发及维护人员，使其能更好的维护和改善系统。	
- 完成日期:2016-07-29

## 项目
- 项目概况
		项目类型：在线视频网站
		网站名称：GiliGili
		开发语言：Python、HTML+CSS+javascript、SQLlite
		开发框架: Django
		
- 开发人员
		截至至本文档完成时间止，本网站由黄子懿，刘子威，许骏洲编写，并引用了若干开源库。
		有关编写人的联系方式以及引用开源库以及其版本信息请见“更多”条目。
- 开发环境
本网站在Windows7/8/10的环境下编写，以下有关开发环境的搭建，均以Windows为准。
为了开发或者维护本网站，你需要先安装以下内容——
> - Python3.5：你可以访问[Python官网](https://www.python.org/)获得Python
> - Django1.9.8：你可以访问<https://www.djangoproject.com/>获得Django，根据安装方式的不同，你可能还安装一些其他Django支持
> - 本项目的调试在Firefox47.0.1以及Chrome51.0.2704.106 m上进行

## 代码
- 基本结构
	- 视频 
	- 用户
作为一个视频网站，本网站的基本结构是由视频和用户的交互构成的，用户可以发布视频，播放视频，评论视频，给视频点赞，管理员用户可以审核视频、封禁视频和解封视频。
- 代码组织
>- glgl  ——django框架的路径等设置
>- glgl_app
>  - template  ——html模版
>  - static  ——静态css,javascript,图片,字体文件
>  - 服务器端代码
>       - video.py  ——视频播放的有关代码
>       - models.py  ——数据建模和从html表单生成的有关代码
>       - views.py  ——与前端页面交互的有关代码
>       - search.py  ——搜索的服务器端代码
>       - django框架自带页面的一些后端代码
>- media  ——用户端向服务器端传送的资源文件存放处

- 模型建立
``` python
class UserExtraProfile(models.Model):
	#django自带的User
	user = models.OneToOneField(User)
	headimage = models.ImageField(upload_to = 'headimages', 
								  default = 'default/defaulthead.jpg')				#头像
	nickName = models.CharField(max_length = 20, default = '')						#昵称
	description = models.CharField(max_length = 50, default = '')					#个人描述
	videoUploaded = models.ManyToManyField("Video", related_name = "videoUploaded")	#上传的视频

#视频
class Video(models.Model):
	title = models.CharField(max_length = 100, default = 'title')				#标题
	video = models.FileField(upload_to = 'videos')								#视频文件
	cover = models.ImageField(upload_to = 'covers', 
							  default = 'default/default.jpg')					#封面
	description = models.CharField(max_length = 200, default = 'description')	#描述
	tag = models.CharField(max_length = 100, default = '', blank = True)		#标签
	uploader = models.ForeignKey(User)											#UP主
	category = models.IntegerField(default = 0)									#类别id
	categoryName = models.CharField(max_length = 20, default = '')				#类别名
	play = models.IntegerField(default = 0)										#播放数
	like = models.IntegerField(default = 0)										#点赞数
	like_list = models.ManyToManyField(UserExtraProfile)						#点赞列表
	time = models.DateTimeField(auto_now = False, auto_now_add = True)			#上传时间
	status = models.IntegerField(default = 0)									#状态

# 评论
class Comment(models.Model):
	user = models.ForeignKey(User)							#评论者
	video = models.ForeignKey(Video)						#评论视频
	content = models.CharField (max_length = 400)			#内容
	cdate = models.DateTimeField(default = timezone.now)	#评论时间

#消息提醒
class Notification(models.Model):
	NContent = models.CharField(max_length=50)
	NUser = models.ForeignKey(UserExtraProfile)
```
- 模型后端接口
```python
#上传视频
def upload(request):
#登录
def login(request, error_msg = ""):
#注册
def register(request, error_msg = ""):
#个人信息
def profile(request, error_msg = ''):
#重设密码
def setPassword(request, error_msg = ""):
#登出
def logout(request):
```
- 视频接口
```python
#播放视频
def video_play(request, video_id):
#视频通过
def video_pass(request, video_id):
#视频封禁
def video_ban(request, video_id):
#添加评论
def video_comment_add(request):
#点赞
def like(request, video_id):
#增加播放量
def play_add(request):
```
- 视图接口
```python
#主页
def index(request):
#分类页
def category(request, category_id):
#个人信息
def home(request):
#更改密码成功
def setPasswordSuc(request):
#个人主页
def homepage(request, user_id):
#审核页面
def checkpage(request):
#封禁页面
def banpage(request):
#更多评论页
def more_comments(request, video_id):
#关于页
def aboutus(request):
```
##更多
- 支持
	为实现多样的样式及功能，我们调用了如下外部库，在html文件的script标签下你可以查看他们的详细信息，
> - layer2
> - bootstrap
> - jqeury
> - video.js
 
- 关于我们
  - 黄子懿:
     - 邮箱: <turquoisehuang@gmail.com>
     - 学号: 2014012106
  - 刘子威
	  - 邮箱: <lzw19951010@126.com>
	  - 学号: 2014013455
  - 许骏洲
	  - 邮箱: <xuxu9110@163.com>
	  - 学号: 2014013465
- GITHUB
  - <https://github.com/lzw19951010/giligili>
  
- 团队分工
  - 依据功能模块的分工方式，三个人工作量基本均等，困难问题共通攻坚。由于公用账号以及调用库和框架的原因，代码量无法通过github直观显示。
