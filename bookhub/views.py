from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from bookhub.utils import hash_password
from .models import User
from .models import Books
from .models import Rating
from .models import Category
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
    user = User(username=username, password=password_hash)
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
        name = data.get('username')
        pwd = data.get('password')
        password_hash = hash_password(pwd)
        print(name, password_hash)
        admin = User.objects.filter(username=name).first()
        if name == admin.username and password_hash == admin.password:
            response_data = {'code': 200, 'message': 'Login success'}
        else:
            response_data = {'code': 400, 'message': 'Login failed'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'code': 400, 'message': 'Invalid request method'})


# get most popular
@csrf_exempt
def getMostPopular(request):
    # TODO: get most popular books here
    data = []

    return JsonResponse({'code': 200, 'message': 'most popular', 'data': data})


# get most rated
@csrf_exempt
def getMostRated(request):
    # TODO: get most rated books here
    data = []

    return JsonResponse({'code': 200, 'message': 'most rated', 'data': data})


# get all books
@csrf_exempt
def getAllBooks(request):
    # TODO: get all books here
    data = []

    return JsonResponse({'code': 200, 'message': 'all books', 'data': data})


# get all categories
@csrf_exempt
def getAllCategories(request):
    # TODO: get all categories here
    data = Category.objects.values()  # 获取Category数据
    return JsonResponse({'code': 200, 'message': 'all categories', 'data': list(data)})


# get recommended books
@csrf_exempt
def getRecommendedBooks(request):
    # TODO: get recommended books here
    data = []

    return JsonResponse({'code': 200, 'message': 'recommended', 'data': data})


# get shopping cart
@csrf_exempt
def getShoppingCart(request):
    # TODO: get shopping cart here
    # user = json.loads(request.body)
    # user_id = user.get('id')
    # TODO: get user's cart info (books ids) by user_id
    data = []

    return JsonResponse({'code': 200, 'message': 'shopping cart', 'data': data})


# get search result
@csrf_exempt
def getSearchResult(request):
    # TODO: get search result here
    # str = json.loads(request.body)
    # TODO: get result by str
    data = []

    return JsonResponse({'code': 200, 'message': 'search', 'data': data})