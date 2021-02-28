from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt

# Create your views here.


def index(request):
    return render(request, "login_reg.html")


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        request.session['user_id'] = new_user.id
        return redirect('/books')


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            if 'login_error' in request.session:
                request.session.pop('login_error')
            request.session['user_id'] = logged_user.id
            return redirect('/books')
        else:
            request.session['login_error'] = 'Email and password does not matching, try again'
            return redirect('/')

    return redirect('/')


def logout(request):
    del request.session['user_id']
    return redirect('/')


def main(request):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "all_books": Book.objects.all(),
    }
    return render(request, "main.html", context)


def addBooks(request):
    errors = Book.objects.basic_validator(request.POST)
    if errors:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/books')
    else:
        logged_user = User.objects.get(id=request.session['user_id'])
        all_books = Book.objects.filter(title=request.POST['title'])
        if len(all_books) < 1:
            Book.objects.create(
                title=request.POST['title'], desc=request.POST['desc'], uploaded_by=logged_user)
        else:
            messages.error(request, "Book was already uploaded by someone")

        book = Book.objects.get(title=request.POST['title'])

        if not logged_user in book.users_who_like.all():
            book.users_who_like.add(logged_user)

        request.session['title'] = request.POST['title']
        return redirect('/books')


def display_book(request, id):
    display_book = Book.objects.get(id=id)
    request.session['title'] = display_book.title
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "book": Book.objects.get(id=id),
        "users_who_like": User.objects.filter(liked_books__in=Book.objects.filter(title=request.session['title']))
    }
    return render(request, "display_book.html", context)


def un_fav(request, id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_book = Book.objects.get(id=id)
    this_user.liked_books.remove(this_book)
    return redirect(f'/books/{id}')


def add_fav(request, id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_book = Book.objects.get(id=id)
    this_user.liked_books.add(this_book)
    return redirect('/books')


def update_delete(request, id):
    if 'update' in request.POST:
        update_book = Book.objects.get(id=id)
        update_book.title = request.POST['title']
        update_book.desc = request.POST['desc']
        update_book.save()
        return redirect(f'/books/{id}')
    elif 'delete' in request.POST:
        delete_book = Book.objects.get(id=id)
        delete_book.delete()
    return redirect('/books')


def user_page(request):
    logged_user = User.objects.get(id=request.session['user_id'])
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "fav_books": logged_user.liked_books.all()
    }
    return render(request, "user.html", context)
