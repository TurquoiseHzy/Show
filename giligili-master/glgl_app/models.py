from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.views.decorators.http import require_http_methods
import django.utils.timezone as timezone
import os 

#用户额外信息
class UserExtraProfile(models.Model):
	user = models.OneToOneField(User)
	headimage = models.ImageField(upload_to = 'headimages', 
								  default = 'default/defaulthead.jpg')				#头像
	nickName = models.CharField(max_length = 20, default = '')						#昵称
	description = models.CharField(max_length = 50, default = '')					#个人描述
	videoUploaded = models.ManyToManyField("Video", related_name = "videoUploaded")	#上传的视频

	def __str__(self):
		return self.user.username

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

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return '/video/%u' % self.pk

# 评论
class Comment(models.Model):
	user = models.ForeignKey(User)							#评论者
	video = models.ForeignKey(Video)						#评论视频
	content = models.CharField (max_length = 400)			#内容
	cdate = models.DateTimeField(default = timezone.now)	#评论时间

	def __str__(self):
		return self.user.username

#消息提醒
class Notification(models.Model):
	NContent = models.CharField(max_length=50)
	NUser = models.ForeignKey(UserExtraProfile)

#上传视频表单
class VideoUploadForm(forms.ModelForm):
	class Meta:
		model = Video
		fields = ['title', 'description', 'cover', 'video', 'tag', 'category']



#上传视频
@require_http_methods(["GET", "POST"])
def upload(request):
	if request.user.is_authenticated():
		if request.method == 'GET':
			return render(request, 'upload.html', 
						  {'form': VideoUploadForm(initial = {'title': "", 
						  									  'description': "", 
						  									  'tag': ""})})
		else:
			#上传视频条件达成
			form = VideoUploadForm(request.POST, request.FILES)
			if form.is_valid():
				categoryList = ['', 'THU校内', '动画', '音乐', '舞蹈', 
								'游戏', '科技', '生活', '娱乐']
				video = form.save(commit = False)
				#管理员上传的视频无需审核
				if request.user.is_staff:
					video.status = 0
				else:
					video.status = 4
				#视频属性设置
				video.category = request.POST['category']
				video.categoryName = categoryList[int(video.category)]
				video.uploader = request.user
				video.save()
				form.save_m2m()
				#超级用户无额外信息
				if not request.user.is_superuser:
					video.uploader.userextraprofile.videoUploaded.add(video)
				return HttpResponseRedirect("/")
			else:
				#表单有误
				return render(request, 'upload.html', {'error': form.errors, 'form': form})
	else:
		#未登录
		return render(request, "login.html", {'error': "请登陆"})

#登录
def login(request, error_msg = ""):
	error_msg = ''
	if request.user.is_authenticated():
		return HttpResponseRedirect("/home/")
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect("/home/")
			else:
				error_msg = '该用户无法正常使用'
				return render(request, "login.html", {'username': username, 'context': error_msg})
		else:
			error_msg = '用户名或密码错误'
			return render(request, "login.html", {'username': username, 'context': error_msg})
	else:
		return render(request, "login.html")

#注册
def register(request, error_msg = ""):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/home/")
	if request.method == 'POST':
		input_is_valid = False
		#收集信息，未填则为空
		username = request.POST['username'] if request.POST['username'] else ""
		password1 = request.POST['password1'] if request.POST['password1'] else ""
		password2 = request.POST['password2'] if request.POST['password2'] else ""
		nickname = request.POST['nickname'] if request.POST['nickname'] else ""
		email = request.POST['email'] if request.POST['email'] else ""
		description = request.POST['description'] if request.POST['description'] else ""
		#判断是否达成注册条件
		error_msg = "错误"
		if not username:
			error_msg = "请输入用户名"
		elif not (password1 and password2):
			error_msg = "请输入密码"
		elif not nickname:
			error_msg = "请输入昵称"
		elif not email:
			error_msg = "请输入邮箱"
		elif not description:
			error_msg = "请输入个人描述"
		elif password1 != password2:
			error_msg = "两次密码不一致"
		elif len(password1) < 6:
			error_msg = "密码长度小于6位"
		elif User.objects.filter(username = username):
			error_msg = "用户名已经存在"
			username = ""
		elif User.objects.filter(email = email):
			error_msg = "邮箱已经注册"
			email = ""
		else:
			#可注册
			input_is_valid = True
			user = User.objects.create_user(username = username, 
											password = password1, 
											email = email)
			user.save()
			thisProfile = UserExtraProfile(user = user, 
										   nickName = nickname, 
										   description = description)
			thisProfile.save()
			return HttpResponseRedirect("/")
		if not input_is_valid :
			#注册信息有误
			return render(request, "register.html", {'error': error_msg, 
													 'username': username, 
													 'nickname': nickname, 
													 'email': email})
	else:
		return render(request, "register.html")

#个人信息
def profile(request, error_msg = ''):
	if request.user.is_authenticated():
		if request.method == 'POST':
			#收集信息，若无则空
			username = request.POST['username']
			password1 = request.POST['password1'] if request.POST['password1'] else ""
			headimage = request.FILES['headimage']
			nickname = request.POST['nickname'] if request.POST['nickname'] else ""
			description = request.POST['description'] if request.POST['description'] else ""
			user = auth.authenticate(username = username, password = password1)
			if user is not None:
				if user.is_active:
					input_is_valid = False
					if not nickname:
						error_msg = "请输入昵称"
					elif not description:
						error_msg = "请输入个人描述"
					else:
						#调整个人信息
						input_is_valid = True
						profile = user.userextraprofile
						profile.headimage = headimage
						profile.nickName = nickname
						profile.description = description
						profile.save()
						return render(request, "home.html", {'context': '信息更改成功'})
					if not input_is_valid :
						return render(request, "home.html", {'context': error_msg})
				else:
					error_msg = '该用户无法正常使用'
					return render(request, "home.html", {'context': error_msg})
			else:
				error_msg = '密码错误'
				return render(request, "home.html", {'context': error_msg})
		else:
			return render(request, "home.html")
	else:
		return render(request, "notlogin.html")

#重设密码
def setPassword(request, error_msg = ""):
	if request.user.is_authenticated() :
		if request.method == 'POST':
			input_is_valid = False
			password = request.POST['password'] if request.POST['password'] else ""
			newpassword1 = request.POST['newpassword1'] if request.POST['newpassword1'] else ""
			newpassword2 = request.POST['newpassword2'] if request.POST['newpassword2'] else ""
			#判断是否达成重设条件
			error_msg = "错误"
			if not password:
				error_msg = "请输入原密码"
			elif not newpassword1:
				error_msg = "请输入新密码"
			elif not newpassword2:
				error_msg = "请确认新密码"
			elif newpassword1 != newpassword2:
				error_msg = "两次密码不一致"
			elif len(newpassword1) < 6:
				error_msg = "密码长度小于6位"
			elif request.user.check_password(password) == False:
				error_msg = "密码错误"
			else:
				#可重设
				input_is_valid = True
				request.user.set_password(newpassword1)
				request.user.save()
				return HttpResponseRedirect("/setpassword-suc")
			if not input_is_valid :
				return render(request, "setpassword.html", {'error': error_msg})
		else:
			return render(request, "setpassword.html")
	else:
		error_msg = "请先登录"
		return render(request, "login.html", {'error': error_msg})

#登出
def logout(request):
	auth.logout(request)
	return render(request, "logout.html")
