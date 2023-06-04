from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from bookhub.utils import hash_password
from .models import User
from .models import Books
from .models import Rating
from .models import Category
from .models import Cart
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
        data_respond = [
            {
                "user_id": admin.user_id,
                "username": admin.username,
                "password": admin.password
            }
        ]
        print(name, password_hash)
        print(admin.username, admin.password)
        print(name == admin.username and password_hash == admin.password)
        if admin and name == admin.username and password_hash == admin.password:
            response_data = {'code': 200, 'message': 'Login success', 'data': data_respond}
        else:
            response_data = {'code': 400, 'message': 'Login failed'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'code': 400, 'message': 'Invalid request method'})


# get most popular
@csrf_exempt
def get_most_popular(request):
    # TODO: get most popular books here
    data = []

    return JsonResponse({'code': 200, 'message': 'most popular', 'data': data})


# get most rated
@csrf_exempt
def get_most_rated(request):
    # TODO: get most rated books here
    data = []

    return JsonResponse({'code': 200, 'message': 'most rated', 'data': data})


# get all books
@csrf_exempt
def get_all_books(request):
    # TODO: get all books here
    # 12 books for demo
    books = Books.objects.all()[:10]

    # convert to json
    data = [
        {
            'bookId': book.bookId,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'category': book.category,
            'year': book.year,
            'price': book.price,
            'img_s': book.img_s,
            'img_m': book.img_m,
            'img_l': book.img_l,
        }
        for book in books
    ]

    return JsonResponse({'code': 200, 'message': 'all books', 'data': data})


# get all categories
@csrf_exempt
def get_all_categories(request):
    # TODO: get all categories here
    data = Category.objects.values()  # 获取Category数据
    return JsonResponse({'code': 200, 'message': 'all categories', 'data': list(data)})


# get recommended books
@csrf_exempt
def get_recommended_books(request):
    # TODO: get recommended books here
    data = []

    return JsonResponse({'code': 200, 'message': 'recommended', 'data': data})


# set shopping cart
@csrf_exempt
def set_shopping_cart(request):
    data = json.loads(request.body)
    data_user_id = data.get("user_id")
    data_book_id = data.get("book_id")
    data_count = data.get("count")

    try:
        Cart.objects.filter(userId=data_user_id, bookId=data_book_id).update(count=data_count)
    except Cart.DoesNotExist:
        newcart = Cart()
        newcart.userId = data_user_id
        newcart.bookId = data_book_id
        newcart.count = data_count
        newcart.save()

    return JsonResponse({'code': 200, 'message': 'success'})


@csrf_exempt
def remove_cart(request):
    user_book = json.loads(request.body)
    print(user_book)
    user_id = user_book.get('user_id')
    book_id = user_book.get('book_id')
    print(type(user_id))
    print(type(book_id))
    # send book_id = -1 if you want to vide cart
    if book_id != -1:
        deleted_count, _ = Cart.objects.filter(userId=user_id, bookId=book_id).delete()
    # 执行删除操作
    else:
        deleted_count, _ = Cart.objects.filter(userId=user_id).delete()

    return JsonResponse({'code': 200, 'message': f'{deleted_count} records deleted'})


# get shopping cart
@csrf_exempt
def get_shopping_cart(request):
    # TODO: get shopping cart here
    user = json.loads(request.body)
    print(request)
    print(request.body)
    user_id = user.get('id')
    print(user_id)
    # TODO: get user's cart info (books ids) by user_id
    # 根据user_id在集合中查找对应的记录
    try:
        record = Cart.objects.filter(userId=user_id)
        print(record)
    except Cart.DoesNotExist:
        return JsonResponse({'code': 200, 'message': 'Record not found'})

    results = []
    for item in record:
        book = Books.objects.get(bookId=item.bookId)
        results.append({
            'user_id': user_id,
            'book_id': book.bookId,
            'count': item.count,
            'title': book.title,
            "author": book.author,
            "publisher": book.publisher,
            "category": book.category,
            "year": book.year,
            "price": book.price,
            "img_s": book.img_s,
            "img_m": book.img_m,
            "img_l": book.img_l,
        })

    return JsonResponse({'code': 200, 'message': 'shopping cart', 'data': results})


# get search result
@csrf_exempt
def get_search_result(request):
    # TODO: get search result here
    str = json.loads(request.body)
    # TODO: get result by str
    data = []

    return JsonResponse({'code': 200, 'message': 'search', 'data': data})


@csrf_exempt
def get_book_detail(request):
    param = json.loads(request.body)
    book_id = param.get("id")
    try:
        book = Books.objects.get(bookId=book_id)
        data = {
            "bookId": book.bookId,
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "category": book.category,
            "year": book.year,
            "price": book.price,
            "img_s": book.img_s,
            "img_m": book.img_m,
            "img_l": book.img_l,
        }
        return JsonResponse({'code': 200, 'message': 'get book details', 'data': data})
    except Books.DoesNotExist:
        return JsonResponse({'code': 404, 'message': 'book not found'})
