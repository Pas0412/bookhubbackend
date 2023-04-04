from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from bookhub.utils import hash_password
from .models import User


# Create your views here.
# Result class general
class R:
    def __init__(self, statecode, message, data=None):
        self.statecode = statecode
        self.message = message
        self.data = data


def index(request):
    return HttpResponse("欢迎使用")


def user_list(request):
    return HttpResponse("用户列表")


def user_add(request):
    return HttpResponse("添加用户")


def sign_up(request):
    username = request.POST.get("user")
    password = request.POST.get("pwd")
    email = request.POST.get("email")
    password_hash = hash_password(password)
    user = User(name=username, email=email, password=password_hash)
    user.save()
    return HttpResponse('User created')


def login(request):
    username = request.POST.get("user")
    password = request.POST.get("pwd")
    password_hash = hash_password(password)
    admin = User.objects.filter(username=username).first()
    print(admin)
    if username == admin.username and password_hash == admin.password:
        r = R(200, "Login success")
    else:
        r = R(400, "Login failed")

    return JsonResponse(r.__dict__)
