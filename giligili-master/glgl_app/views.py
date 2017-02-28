from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from glgl_app.models import *

@require_http_methods(["GET"])
def index(request):
	return render(request, "index.html", 
				  context = {'popular_videos': Video.objects.filter(status = 0).order_by("-play")[:16], 
							 'pageTitle': '首页'})

@require_http_methods(["GET"])
def category(request, category_id):
	categoryList = ['', 'THU校内', '动画', '音乐', '舞蹈', '游戏', '科技', '生活', '娱乐']
	return render(request, "index.html", 
				  context = {'category_videos': Video.objects.filter(status = 0, category = category_id), 
							 'pageTitle': categoryList[int(category_id)]})

@require_http_methods(["GET"])
def home(request):
	return render(request, "home.html")

@require_http_methods(["GET"])
def setPasswordSuc(request):
	return render(request, "setpassword-suc.html")

@require_http_methods(["GET"])
def homepage(request, user_id):
	try:
		user = User.objects.get(pk = user_id)
	except User.DoesNotExist:
		raise Http404("User does not exist")
	return render(request, 'homepage.html', 
				  {'pageuser': user, 
				   'video_set': user.video_set.all().filter(status = 0).order_by("-time")})

@require_http_methods(["GET"])
def checkpage(request):
	if not request.user.is_staff:
		return render(request, 'notadmin.html')
	else:
		return render(request, 'check.html', 
					  context = {'checking_videos': Video.objects.filter(status = 4).order_by("time")})

@require_http_methods(["GET"])
def banpage(request):
	if not request.user.is_staff:
		return render(request, 'notadmin.html')
	else:
		return render(request, 'banvideo.html', 
					  context = {'checking_videos': Video.objects.filter(status = 2).order_by("time")})

@require_http_methods(["GET"])
def more_comments(request, video_id):
	if not request.user.is_authenticated:
		return render(request, 'video.html')
	else:
		video = Video.objects.get(pk = video_id)
		comments = video.comment_set.all().order_by("-cdate")
		return render(request, 'more_comments.html', 
					  context = {'video':video, 'all_comment':comments})
		
def aboutus(request):
	return render(request,'about.html')
		