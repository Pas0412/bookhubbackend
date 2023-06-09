"""bookhubbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bookhub import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('signup/', views.sign_up),
    path('popular/', views.get_most_popular),
    path('rated/', views.get_most_rated),
    path('all/', views.get_all_books),
    path('cart/', views.get_shopping_cart),
    path('categories/', views.get_all_categories),
    path('search/', views.get_search_result),
    path('detail/', views.get_book_detail),
    path('setcart/', views.set_shopping_cart),
    path('addtocart/', views.add_to_cart),
    path('removecart/', views.remove_cart),
    path('favorite/', views.get_favorite_list),
    path('setfavorite/', views.set_favorite_list),
    path('isfavorite/', views.is_favorite),
    path('recommendbybook/', views.recommend_by_book),
    path('setrate/', views.set_rate),
    path('bought/', views.get_bought_list)
]
