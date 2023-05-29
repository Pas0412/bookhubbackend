from djongo import models


class User(models.Model):
    name = models.CharField(max_length=100)
    # email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'bookhub'


class BookCategory(models.Model):
    name = models.CharField(max_length=100, db_column="name")
# Create your models here.


class Books(models.Model):
    bookId = models.CharField(max_length=100, db_column="ISBN")
    title = models.CharField(max_length=100, db_column="Book-Title")
    author = models.CharField(max_length=100, db_column="Book-Author")
    publisher = models.CharField(max_length=100, db_column="Publisher")
    category = models.CharField(max_length=100, db_column="Category")
    year = models.IntegerField(max_length=4, db_column="Year-Of-Publication")
    price = models.CharField(max_length=10, db_column="Price")
    img_s = models.CharField(max_length=100, db_column="Image-URL-S")
    img_m = models.CharField(max_length=100, db_column="Image-URL-M")
    img_l = models.CharField(max_length=100, db_column="Image-URL-L")
