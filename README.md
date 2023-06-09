# BookHub back-end
backend for bookhub using Django and Python

video of presentation: https://youtu.be/z4Pml66kBuk

Author : [![](https://img.shields.io/badge/@Pas0412-grey)](https://github.com/Pas0412)

Project of DS50 UTBM 2023 ：Web e-commerce with recommandation algorithm （KNN）

![](https://img.shields.io/badge/IDE-PyCharm-lightgreen?style=flat&logo=pycharm)
![](https://img.shields.io/badge/Platform-MacOS&emsp;Ventura&emsp;13.0.1-000000?style=flat&logo=apple)

![](https://img.shields.io/badge/Python-v3.9-3776AB?style=for-the-badge&logo=python)
![](https://img.shields.io/badge/Django-v4.1.7-092E20?style=for-the-badge&logo=django)
![](https://img.shields.io/badge/MongoDB-v4.0.9-47A248?style=for-the-badge&logo=mongodb)
![](https://img.shields.io/badge/Djongo-v1.3.6-lightblue?style=for-the-badge&logo=django)

## MAKE DATABASE CHANGES:

### Using Python3.9
``` bash
# 
python3.9 manage.py makemigrations bookhub

# 
python3.9 manage.py migrate bookhub
```

## TABLE

###  USER

###  CATEGORY

###  RATING

###  BOOKS

###  CART

## FUNCTION

### SIGN UP
   - password encoding

### LOG IN
   - password encoding

### DISPLAY BOOKS
   - recommend books(most rated, most popular, recommendation based on one book using KNN)
   - books by category
   - book detail
   - is favorite judgment
   - get rate
   - show more

### CART
   - set cart
   - get cart
   - remove cart by book/all
   - payment

### FAVORITE
   - get favorite list
   - set favorite
   - remove favorite

### RATING
   - rating books(set rate)

### SEARCH
   - get search result
   - show more

### HISTORY
   - get history of buying

## FOLDER STRUCTURE TREE
<img width="310" alt="截屏2023-06-12 10 56 39" src="https://github.com/Pas0412/bookhubbackend/assets/68329670/f5910449-d498-4317-bdd1-3d528c77bb9e">

   - models.py
      collection mapping
   - views.py
      APIs
   - utils.py
      functions used in API (algorithm)
   - setting.py
      settings (registration of app, connection settings with MongoDB)
   - urls.py
      urls of APIs

## DEPENDENCIES
``` bash
# pymongo
pip install pymongo

# djongo
pip install djongo

# setting.py

```

