from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, UserManager, Secret, SecretManager
from django.contrib import messages
from django.db.models import Count

def index(request):
    return render(request, 'dojo_secrets_app/index.html')

def register(request):
    postData = {
        "first_name" : request.POST['first_name'],
        "last_name" : request.POST['last_name'],
        "email" : request.POST['email'],
        "password" : request.POST['password'],
        "conpass" : request.POST['conpass']
    }
    new_user = User.objects.register(postData)

    if len(new_user) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = postData['first_name']
        return redirect('/secrets')
    else:
        for error in new_user:
            messages.info(request, error)
    return redirect('/')

def login(request):
    postData = {
        "email" : request.POST['email'],
        "password" : request.POST['password'],
    }
    login_validation = User.objects.login(postData)
    #if login is valid return redirect('dojo_secrets_app/secrets.html')t
    if len(login_validation) == 0:
        request.session['id'] = User.objects.get(email=postData['email']).id
        request.session['name'] = User.objects.get(email=postData['email']).first_name
        return redirect('/secrets')
        # return render(request, 'dojo_secrets_app/secrets.html')
    #if login is not valid return redirect('/')
    for error in login_validation:
        messages.info(request, error)
        print "something happened"
        return redirect('/')

def secrets(request):
    a1 = Secret.objects.all().order_by("-created_at")[:5]
    context = {
        "secrets" : a1,
        "currentuser" : User.objects.get(id=request.session['id'])
    }
    print a1
    return render(request, 'dojo_secrets_app/secrets.html', context)


def post(request):
    print request.POST['your_secret_here']
    print request.session['id']
    postData = {
        "secret" : request.POST['your_secret_here'],
        "user_id" : request.session['id'],
    }
    s1 = Secret.objects.post_secret(postData)
    for error in s1:
        message.error(request, error)
    return redirect('/secrets')

def like(request, id, sentby):
    result = Secret.objects.like_secret(id, request.session['id'])
    if result[0] == False:
        messages.error(request, result[1])
    if sentby == "sec":
        return redirect('/secrets')
    else:
        return redirect('/popular')

def delete(request, id, sentby):
    result = Secret.objects.delete_secret(id, request.session['id'])
    if result[0] == False:
        messages.error(request, result[1])
    if sentby == "sec":
        return redirect('/secrets')
    else:
        return redirect('/popular')

def popular(request):
    a1 = Secret.objects.annotate(num_likes=Count('likers')).order_by('-num_likes')[:5]
    context = {
        "secrets" : a1,
        "currentuser" : User.objects.get(id=request.session['id'])
    }
    print a1
    return render(request, 'dojo_secrets_app/popular.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')
