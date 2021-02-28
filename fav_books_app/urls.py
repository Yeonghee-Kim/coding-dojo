from django.urls import path
from . import views

urlpatterns = [
    # GET
    path('', views.index),
    path('books', views.main),
    path('logout', views.logout),
    path('books/<int:id>', views.display_book),
    path('un_fav/<int:id>', views.un_fav),
    path('add_fav/<int:id>', views.add_fav),
    path('user_page', views.user_page),

    # ACTION
    path('register', views.register),
    path('login', views.login),
    path('addBooks', views.addBooks),
    path('update_delete/<int:id>', views.update_delete),
]
