from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# email must be formatted properly

class UserManager(models.Manager):
    # VALIDATION FOR REGISTRATION
    def reg_validator(self, postData):
        errors = {}
    #------ Names ------
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name must be at least 3 characters long!"
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last name must be at least 3 characters long!"
    #------- Email -------
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please input a valid email address!"
        else:
            # searches for email in DB to see if it already exists
            for user in User.objects.all(): 
                if postData['email'] == user.email:
                    errors['email'] = "Email already exists in our system! Please login in!"
    #------- Password -------
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long!"
        elif postData['password'] != postData['pass_conf']:
            errors['pass_conf'] = "Passwords do not match!"
        return errors

    # VALIDATION FOR LOGIN
    def log_validator(slef, postData):
        errors = {}
        # queries for user in DB based on the input email
        # if email not in DB or there is not a proper input, validation will be hit
        user_info = User.objects.filter(email = postData['email_input'])
        if not user_info:
            errors['email_input'] = "Email does not exist! Please register before logging in!"
        else:
            # query for user based on email input
            user = User.objects.get(email=postData['email_input']) 
            if not bcrypt.checkpw(postData['password_input'].encode(), user.password.encode()):
                errors['password_input'] = "Password or Email information is not correct!"
        return errors
    
    # VALIDATION TO SEE IF USER IS LOGGED INTO SITE
    def not_logged_validator(self):
        errors = {}
        errors['no'] = "Please login before entering site!"
        return errors

class TripManager(models.Manager):
    # VALIDATION FOR CREATING/EDITTING A TRIP
    def trip_validator(self, postData):
        errors = {}
        #---- Destination ----
        if len(postData['dest']) < 2:
            errors['dest'] = "Please enter a valid location!"
        #----- Dates -----
        if len(postData['start']) < 1:
            errors['start'] = "Please enter a start date!"
        if len(postData['end']) < 1:
            errors['end'] = "Please enter a end date!"
        #----- Plan -----
        if len(postData['plan']) < 10:
            errors['plan'] = "Please enter a plan that is at least 10 characters long!"
        return errors


class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #created_trips --> related to 'creator' field in Trip model
    objects = UserManager()

class Trip(models.Model):
    dest=models.CharField(max_length=255)
    start=models.DateField()
    end=models.DateField()
    plan=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    creator=models.ForeignKey(User, related_name="created_trips", on_delete=models.CASCADE)
    objects = TripManager()
