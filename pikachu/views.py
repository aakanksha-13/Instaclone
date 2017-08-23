# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from pokemon.settings import BASE_DIR
from pikachu.models import UserModel,SessionToken,PostModel, LikeModel, CommentModel
from .forms import SignupForm,LoginForm, PostForm, LikeForm, CommentForm

from imgurpython import ImgurClient
# Create your views here.
#function  for signup page!!!
def signup_view(request):
    today = datetime.now()
    if request.method == 'GET':
        form=SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashed_password = make_password(password)
             # saving data to DB
            user = UserModel( email=email, name=name, username=username,password=make_password(password))
            user.save()

            return render(request,"success.html")

            return redirect('login/')
    return render(request,'index.html' ,
                      {"today":today,
                        "method":request.method,
                        "form" :form,
                    })

# Function for login page

def login_view(request):

    response_data = {}
    if request.method =='GET':
        form = 'LoginForm'

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:
                # Check for the password
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    response_data['form'] = form
    return render(request, 'login.html', response_data)




def feed_view(request):
    return render(request, 'feed.html')


def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
           return session.user
    else:
        return None


# Function for post validation page
def post_view(request):
        user = check_validation(request)

        if user:
            print 'Authentic user'

        else:
            return redirect('/login/')


# Function for post page
def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + post.image.url)

                client = ImgurClient("9b343edd01f55e8","1a3e10f52540455f2feabd17ca49b2fbaa3aa08b")
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()

                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')


def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:

        return redirect('/login/')


def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')


def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None