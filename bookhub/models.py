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
