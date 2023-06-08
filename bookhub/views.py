from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from bookhub.utils import hash_password, knn_find_neighbors
from .models import User
from .models import Books
from .models import Rating
from .models import Category
from .models import Cart
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Avg, Count
from decimal import Decimal, ROUND_HALF_UP


# Create your views here.
# Result class general
class R:
    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data


# function of avg rating
def get_average_rating(book_id):
    try:
        average_rating = Rating.objects.filter(bookId=book_id, rating__gt=0).aggregate(avg_rating=Avg('rating'))
    except Rating.DoesNotExist:
        return 0

    if average_rating['avg_rating'] is None:
        return 0
    else:
        return Decimal(average_rating['avg_rating'] / 2).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)


@csrf_exempt
def sign_up(request):
    req = json.loads(request.body)
    username = req.get("username")
    password = req.get("password")
    password_hash = hash_password(password)
    # 检查用户名是否已存在
    if User.objects.filter(username=username).exists():
        return JsonResponse({'code': 200, 'message': 'sign up failed'})

    # 获取当前最大的userId
    max_user = User.objects.order_by('-user_id').first()

    # 计算新用户的userId
    new_user_id = max_user.user_id + 1 if max_user else 1

    # 创建新用户
    new_user = User(user_id=new_user_id, username=username, password=password_hash)
    new_user.save()

    return JsonResponse({'code': 200, 'message': 'user created'})


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
    popular_books = Rating.objects.values('bookId').annotate(popularity=Count('bookId')).order_by('-popularity')[:12]
    book_ids = [book['bookId'] for book in popular_books]

    get_books_info = Books.objects.filter(bookId__in=book_ids)

    serialized_data = []
    for book in get_books_info:
        serialized_data.append({
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
        })
    print(serialized_data)

    return JsonResponse({'code': 200, 'message': 'most popular', 'data': serialized_data})


# get most rated
@csrf_exempt
def get_most_rated(request):
    # get most rated books here
    top_books = Rating.objects.values('bookId').annotate(avg_rating=Avg('rating')).order_by('-avg_rating')[:12]
    book_ids = [book['bookId'] for book in top_books]
    top_rated_books = Books.objects.filter(bookId__in=book_ids)

    serialized_data = []
    for book in top_rated_books:
        serialized_data.append({
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
        })
    print(serialized_data)

    return JsonResponse({'code': 200, 'message': 'most rated', 'data': serialized_data})


# get all books
@csrf_exempt
def get_all_books(request):
    # get all books here
    req = json.loads(request.body)
    cat = req.get('category')
    nb = req.get('nb')
    print('cat:' + cat)
    books = Books.objects.filter(category=cat)[:nb]

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
    # get all categories here
    data = Category.objects.values()  # 获取Category数据
    return JsonResponse({'code': 200, 'message': 'all categories', 'data': list(data)})


# Add to cart
@csrf_exempt
def add_to_cart(request):
    data = json.loads(request.body)
    data_user_id = data.get("user_id")
    data_book_id = data.get("book_id")


    cart = Cart.objects.filter(userId=data_user_id, bookId=data_book_id)
    if cart:
        count_temp = cart.values('count')[0]['count'] + 1
        cart.update(count=count_temp)
    else:
        new_cart = Cart()
        new_cart.userId = data_user_id
        new_cart.bookId = data_book_id
        new_cart.count = 1
        new_cart.save()

    return JsonResponse({'code': 200, 'message': 'added to cart'})


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
        cart = Cart()
        cart.userId = data_user_id
        cart.bookId = data_book_id
        cart.count = data_count
        cart.save()

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
        books = Cart.objects.filter(userId=user_id).values('bookId')
        book_ids = [book['bookId'] for book in books]
        for bid in book_ids:
            Rating.objects.filter(userId=user_id, bookId=bid, bought=0).update(bought=1)
        deleted_count, _ = Cart.objects.filter(userId=user_id).delete()

    return JsonResponse({'code': 200, 'message': f'{deleted_count} records deleted'})


# get shopping cart
@csrf_exempt
def get_shopping_cart(request):
    user = json.loads(request.body)
    print(request)
    print(request.body)
    user_id = user.get('id')
    print(user_id)
    # get user's cart info (books ids) by user_id
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
    req = json.loads(request.body)
    search_string = req.get("search")
    search_nb = req.get("nb")
    matching_books = Books.objects.filter(title__icontains=search_string)[:search_nb]
    book_ids = [book.bookId for book in matching_books]

    get_books_info = Books.objects.filter(bookId__in=book_ids)

    serialized_data = []
    for book in get_books_info:
        serialized_data.append({
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
        })
    print(serialized_data)

    return JsonResponse({'code': 200, 'message': 'search', 'data': serialized_data})


@csrf_exempt
def get_book_detail(request):
    param = json.loads(request.body)
    book_id = param.get("id")
    try:
        book = Books.objects.get(bookId=book_id)
        note = get_average_rating(book_id)
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
            "rate": note
        }
        return JsonResponse({'code': 200, 'message': 'get book details', 'data': data})
    except Books.DoesNotExist:
        return JsonResponse({'code': 404, 'message': 'book not found'})


# set favorite list
@csrf_exempt
def set_favorite_list(request):
    data = json.loads(request.body)
    data_user_id = data.get("user_id")
    data_book_id = data.get("book_id")
    data_like = data.get("like")

    try:
        Rating.objects.filter(userId=data_user_id, bookId=data_book_id).update(like=data_like)
    except Rating.DoesNotExist:
        favorite = Rating()
        favorite.userId = data_user_id
        favorite.bookId = data_book_id
        favorite.rating = 0
        favorite.like = data_like
        favorite.bought = 0
        favorite.save()

    return JsonResponse({'code': 200, 'message': 'success'})


# get favorite list
@csrf_exempt
def get_favorite_list(request):
    # get favorite list here
    user = json.loads(request.body)
    user_id = user.get('id')
    # get user's favorite info by user_id
    # 根据user_id在集合中查找对应的记录
    try:
        record = Rating.objects.filter(userId=user_id, like=1)
    except Rating.DoesNotExist:
        return JsonResponse({'code': 200, 'message': 'Record not found'})

    results = []

    for item in record:
        book = Books.objects.get(bookId=item.bookId)
        results.append({
            'user_id': user_id,
            'book_id': book.bookId,
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


# if user favorite this book
@csrf_exempt
def is_favorite(request):
    req = json.loads(request.body)
    data_user_id = req.get('user_id')
    data_book_id = req.get('book_id')

    try:
        data = Rating.objects.get(userId=data_user_id, bookId=data_book_id)
    except Rating.DoesNotExist:
        data = Rating()
        data.userId = data_user_id
        data.bookId = data_book_id
        data.rating = 0
        data.like = 0
        data.bought = 0
        data.save()

    res = 0
    if data.like == 1:
        res = 1

    return JsonResponse({'code': 200, 'message': 'success', 'data': res})


@csrf_exempt
def recommend_by_book(request):
    req = json.loads(request.body)
    data_book_id = req.get('book_id')

    res = []
    res_list = knn_find_neighbors(data_book_id)
    print(res_list)
    for book_id in res_list:
        book = Books.objects.filter(bookId=book_id).first()  # 在Books集合中查找匹配的书籍
        if book:
            res.append(book)

    processed_res = []
    for book in res:
        book_data = {
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
        processed_res.append(book_data)

    print(processed_res)

    return JsonResponse({'code': 200, 'message': 'success', 'data': processed_res})


@csrf_exempt
def get_bought_list(request):
    # get bought list here
    user = json.loads(request.body)
    user_id = user.get('id')
    # get user's bought info by user_id
    # 根据user_id在集合中查找对应的记录
    try:
        record = Rating.objects.filter(userId=user_id, bought=1)
    except Rating.DoesNotExist:
        return JsonResponse({'code': 200, 'message': 'Record not found'})

    results = []

    for item in record:
        book = Books.objects.get(bookId=item.bookId)
        rate = Rating.objects.get(userId=user_id, bookId=item.bookId)
        results.append({
            'user_id': user_id,
            'book_id': book.bookId,
            'rate': Decimal(rate.rating/2),
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


@csrf_exempt
def set_rate(request):
    req = json.loads(request.body)
    data_user_id = req.get("user_id")
    data_book_id = req.get("book_id")
    data_rate = req.get("rate")

    Rating.objects.filter(userId=data_user_id, bookId=data_book_id).update(rating=data_rate)

    return JsonResponse({'code': 200, 'message': 'success'})
