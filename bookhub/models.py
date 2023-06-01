from djongo import models


class User(models.Model):
    user_id = models.IntegerField(db_column="User-ID")
    username = models.CharField(max_length=100, db_column="Username")
    password = models.CharField(max_length=100, db_column="Password")

    class Meta:
        db_table = 'User'


class Category(models.Model):
    cat_id = models.IntegerField(db_column="Category-ID")
    name = models.CharField(max_length=100, db_column="Category")

    class Meta:
        db_table = 'Category'


class Books(models.Model):
    bookId = models.CharField(max_length=100, db_column="ISBN")
    title = models.CharField(max_length=100, db_column="Book-Title")
    author = models.CharField(max_length=100, db_column="Book-Author")
    publisher = models.CharField(max_length=100, db_column="Publisher")
    category = models.CharField(max_length=100, db_column="Category")
    year = models.IntegerField(db_column="Year-Of-Publication")
    price = models.IntegerField(db_column="Price")
    img_s = models.CharField(max_length=100, db_column="Image-URL-S")
    img_m = models.CharField(max_length=100, db_column="Image-URL-M")
    img_l = models.CharField(max_length=100, db_column="Image-URL-L")

    class Meta:
        db_table = 'Books'


class Rating(models.Model):
    userId = models.CharField(max_length=100, db_column="User-ID")
    bookId = models.CharField(max_length=100, db_column="ISBN")
    rating = models.IntegerField(db_column="Book-Rating")
    like = models.IntegerField(db_column="Favorite")

    class Meta:
        db_table = 'Rating'