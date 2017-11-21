# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = 'name should be longer than 2 characters'
        if len(postData['alias']) < 2:
            errors['alias'] = 'alias name should be longer than 2 characters'
        if len(postData['email']) < 1:
            errors['email'] = 'email is required'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'email must be in valid format'
        if len(User.objects.filter(email=postData['email'])) >= 1:
            errors['validEmail'] = 'email already in use'
        if postData['password'] != postData['confirmPassword']:
            errors['confirm'] = 'both passwords must match!'
        if len(postData['password']) < 8:
            errors['password'] = 'password must be greater than 8 characters'
        if len(postData['birthday']) < 9:
            errors['birthday'] = "Please enter your birthdate"
        return errors

    def validate_login(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['email'] = 'Email is required'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be in valid format'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be greater than 8 characters'
        if len(User.objects.filter(email=postData['email'])) < 1:
            errors['validEmail'] = 'Please register first'
        else:
            password = postData['password']
            email = postData['email']
            print password
            user = User.objects.get(email=email)
            print user.password
            hashed = user.password
            if not bcrypt.checkpw(password.encode(), hashed.encode()):
                errors['validPassword'] = 'Please enter the correct password'
        return errors

    def validate_quote(self, postData):
        errors = {}
        if len(postData['quotedBy']) < 3:
            errors['content'] = 'Quotes should be longer than 3 characters'
        if len(postData['content']) < 10:
            errors['content'] = 'Message should be more than 10 characters'
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateTimeField(blank=False, default=datetime.now())
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Quote(models.Model):
    content = models.CharField(max_length=255)
    quoted_by = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='quote')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Favorites(models.Model):
    quote = models.ForeignKey(Quote, related_name='favorites')
    user = models.ForeignKey(User, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
