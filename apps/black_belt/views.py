# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt
from django.db.models import Count

def index(request):
    return render(request, 'black_belt/index.html')

def register(request):
    error = User.objects.validate_registration(request.POST)
    if len(error):
        for tag, error in error.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        name = request.POST['name']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['password']
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(name=name, alias=alias, email=email, password=password)
        request.session['user'] = user.alias
        request.session['id'] = user.id
        return redirect('/quotes')

def login(request):
    error = User.objects.validate_login(request.POST)
    if len(error):
        for tag, error in error.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user'] = user.alias
        request.session['id'] = user.id
        print request.session['id']
        return redirect('/quotes')

def quotes(request):
    user = User.objects.get(id=request.session['id'])
    quote = Quote.objects.all().order_by('-id')
    favorite = Favorites.objects.filter(user=user)
    context = {
        'user':user,
        'quotes':quote,
        'favorites':favorite
    }
    return render(request, 'black_belt/quotes.html', context)

def process(request):
    if request.method == 'POST':
        error = User.objects.validate_quote(request.POST)
        if len(error):
            for tag, error in error.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/quotes')
        else:
            userObject = User.objects.get(id=request.session['id'])
            print userObject
            quotedBy = request.POST['quotedBy']
            content = request.POST['content']
            Quote.objects.create(content=content, quoted_by=quotedBy, user=userObject)
            return redirect('/quotes')
    else:
        return redirect('/quotes')

    return redirect('/quotes')

def favorite(request):
    quoteID = request.POST['quoteObj']
    quoteObject = Quote.objects.get(id=quoteID)
    userID = request.session['id']
    print userID
    userObject = User.objects.get(id=userID)
    Favorites.objects.create(quote=quoteObject, user=userObject)
    return redirect('/quotes')

def viewUser(request, id):
    user = User.objects.annotate(count=Count('quote')).get(id=id)
    userObject = User.objects.get(id=id)
    quotes = Quote.objects.filter(user=userObject)
    content = {
        'user':user,
        'quotes':quotes
    }
    return render(request, 'black_belt/user.html', content)

def removeFavorite(request):
    favoriteID = request.POST['quote']
    favoriteObject = Favorites.objects.get(id=favoriteID)
    favoriteObject.delete()
    return redirect('/quotes')

def logout(request):
    def logout(request):
        request.session.clear()
    return redirect('/')
