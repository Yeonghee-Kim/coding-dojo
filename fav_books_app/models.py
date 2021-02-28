from django.db import models
import re
# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # Email Regex
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name should be at least 2 characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name should be at least 2 characters'

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address!'
        if User.objects.filter(email=postData['email']).exists():
            errors['user'] = 'Email already exists'

        if len(postData['password']) and len(postData['confirm_pw']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = 'Enter the same password as before'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if postData['title'] == "":
            errors['title'] = "Title is required"
        if len(postData['desc']) < 5:
            errors['desc'] = "Description must be at least 5 characters"
        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(
        User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookManager()
