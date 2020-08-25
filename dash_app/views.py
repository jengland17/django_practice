from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from django.db.models import Q
from .models import *

# Create your views here.
def index(request):

    return render(request, "index.html")

def register(request):

    reg_errors = User.objects.register_validator(request.POST)

    if len(reg_errors) > 0:
        for key, value in reg_errors.items():
            messages.error(request, value)
            return redirect("/")
    else:

        secure_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(first_name = request.POST['form_first'], last_name = request.POST['form_last'], email = request.POST['form_email'], password = secure_password)

        request.session['user'] = new_user.id

    return redirect("/quotes")

def login(request):
    
    login_errors = User.objects.login_validator(request.POST)

    if len(login_errors) > 0:
        for key, value in login_errors.items():
            messages.error(request, value)
            return redirect("/")
    else:

        email_match = User.objects.filter(email = request.POST['form_email'])

        request.session['user'] = email_match[0].id
    
    return redirect("/quotes")

def quotes(request):

    if 'user' not in request.session:
        return redirect("/")
    
    else:
        context = {
            'user_in': User.objects.get(id=request.session['user']),
            'allquotes': Post.objects.all(),
            'userDelete': Post.objects.filter(users = User.objects.get(id=request.session['user'])) 
        }

    return render(request, "quotes.html", context)

def addQuote(request):

    post_errors = Post.objects.post_validator(request.POST)

    if len(post_errors) > 0:
        for key, value in post_errors.items():
            messages.error(request, value)
            return redirect("/quotes")

    else:

        Post.objects.create(author = request.POST['form_author'], quote = request.POST['form_quote'], uploader = User.objects.get(id=request.session['user']))

    return redirect("/quotes")

def editAccountPage(request, idUser):

    context = {
        'userToEdit': User.objects.get(id=idUser)
    }

    return render(request, "edit.html", context)

def editUser(request, idUser):

    edit_errors = User.objects.edit_validator(request.POST)

    if len(edit_errors) > 0:
        for key, value in edit_errors.items():
            messages.error(request, value)
            return redirect(f"/myaccount/{idUser}/edit")
    
    else:

        user = User.objects.get(id=idUser)

        user.first_name = request.POST['form_first']
        user.last_name = request.POST['form_last']
        user.email = request.POST['form_email']  
        user.save()

    return redirect("/quotes")

def viewUser(request, idUser):

    context = {
        'user': User.objects.get(id=idUser)
    }

    return render(request, "user.html", context)

def likeQuote(request, quoteId):

    liker = User.objects.get(id=request.session['user'])
    quote = Post.objects.get(id=quoteId)

    quote.users.add(liker)

    return redirect("/quotes")

def removePost(request, quoteId):

    deletePost = Post.objects.get(id=quoteId)

    deletePost.delete()

    return redirect("/quotes")

def destory(request):

    request.session.clear()

    return redirect("/")