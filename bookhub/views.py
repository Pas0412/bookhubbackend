from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from bookhub.utils import hash_password
from .models import User
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
# Result class general
class R:
    def __init__(self, code, message, data=None):
        self.code = code
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
    # email = request.POST.get("email")
    password_hash = hash_password(password)
    user = User(name=username, password=password_hash)
    user.save()
    return HttpResponse('User created')


@csrf_exempt
def login(request):
    # if request.method == 'OPTIONS':
    #     response = HttpResponse()
    #     response['Access-Control-Allow-Origin'] = '*'
    #     response['Access-Control-Allow-Methods'] = 'POST'
    #     response['Access-Control-Allow-Headers'] = 'Content-Type'
    #     return response
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        password_hash = hash_password(password)
        print(username, password_hash)
        admin = User.objects.filter(name=username).first()
        if admin and username == admin.name and password_hash == admin.password:
            response_data = {'code': 200, 'message': 'Login success'}
        else:
            response_data = {'code': 400, 'message': 'Login failed'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'code': 400, 'message': 'Invalid request method'})
