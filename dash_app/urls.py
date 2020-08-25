from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('quotes', views.quotes),
    path('addQuote', views.addQuote),
    path('myaccount/<int:idUser>/edit', views.editAccountPage),
    path('updateUser/<int:idUser>', views.editUser),
    path('user/<int:idUser>', views.viewUser),
    path('likepost/<int:quoteId>', views.likeQuote),
    path('remove/<int:quoteId>', views.removePost),
    path('log_out', views.destory)
]