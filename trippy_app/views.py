from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


# ============================================
# Login/Registration
# ============================================

def index(request):
    # nothing to add to context b/s login/registration is rendered on the index.html
    return render(request, 'index.html')

def register(request):
    # verify that this route is being handled after a form submission (i.e. POST route)
    if request.POST:
        # handles errors specifically for registration fields
        errors = User.objects.reg_validator(request.POST)
        # check if any errors were added and passed forward
        if len(errors):
            for key, value in errors.items():
                # pass forward 'key' values as 'extra_tags' so jinja can access on the front and access specific errors
                messages.error(request, value, extra_tags=key)
            # redirect back to root route, where error messages will be rendered
            return redirect('/')

        # if there are no errors
        else:
            # create the new user based on registration information, only if no errors are hit
            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                # hash password prior to entering into database
                password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )

            # put new user's id into session, so it can ba accessed later
            request.session['user_id'] = user.id
            return redirect('/dashboard')

    else: 
        # redirect back to root route if route is accessed outside of POST
        return redirect('/')

def login(request):
    # verify that this route is being handled after a form submission (i.e. POST route)
    if request.POST:
        # handles errors specifically for login fields
        errors = User.objects.log_validator(request.POST)
        # check if any errors were added and passed forward
        if len(errors):
            # pass forward 'key' values as 'extra_tags' so jinja can access on the front and access specific errors
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            # redirect back to root route, where error messages will be rendered
            return redirect('/')

        # if there are no errors    
        else:
            # query for user based on the email that was provided 
            user = User.objects.get(email=request.POST['email_input'])
            # add user id into session so you can access is later
            request.session['user_id'] = user.id
            return redirect('/dashboard')

    else: 
        # redirect back to root route if route is accessed outside of POST
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

# ============================================
# Dashboard
# ============================================

def dashboard(request):
    # verify that there is a user id in session
    # if there is no user id in session, it means no one is properly logged in and should be redirected back to the log/reg page
    if 'user_id' not in request.session:
        errors = User.objects.not_logged_validator()
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:
        # query for user based on user_id in seesion
        user = User.objects.get(id=request.session['user_id'])
        # pass user forward, as well as all trips
        context = {
            'user' : user,
            'trips' : Trip.objects.all()
        }
        return render(request, 'dashboard.html', context)

# ============================================
# Create Trip
# ============================================

def create_trip(request):
    # verify that there is a user id in session
    # if there is no user id in session, it means no one is properly logged in and should be redirected back to the log/reg page
    if 'user_id' not in request.session:
        errors = User.objects.not_logged_validator()
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:
        # first, pull the user id from session
        user_id = request.session['user_id']
        # query for user based on user id
        user = User.objects.get(id=user_id)
        # pass user information forward
        context = {
            'user' : user
        }
        return render(request, 'create.html', context)

def new_trip(request):
    # verify that this route is being handled after a form submission (i.e. POST route)
    if request.POST:
        # handles errors specifically for trip fields
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors):
            # pass forward 'key' values as 'extra_tags' so jinja can access on the front and access specific errors
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            # redirect back to trip creation page where errors will be rendered with html
            return redirect('/trips/new')

        # if there are no errors
        else:
            # query for user based on user_id in session
            user = User.objects.get(id=request.session['user_id'])
            # create new trip based on information input into form
            trip = Trip.objects.create(
                dest=request.POST['dest'],
                start=request.POST['start'],
                end=request.POST['end'],
                plan=request.POST['plan'],
                creator=user
            )
            # redirect back to dashboard, where new trip should be displayed
            return redirect('/dashboard')

    # if route accessed not on a POST
    else:
        # redirect back to dashboard where nothing should have changed
        return redirect('/dashboard')

# ============================================
# Show Trip
# ============================================

def show_trip(request, id):
    # verify that there is a user id in session
    # if there is no user id in session, it means no one is properly logged in and should be redirected back to the log/reg page
    if 'user_id' not in request.session:
        errors = User.objects.not_logged_validator()
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:
        # query for user based on user_id in session
        user = User.objects.get(id=request.session['user_id'])
        # pass forward user info, as well as all trip specified by id in url
        context = {
            'user' : user,
            'trip' : Trip.objects.get(id=id)
        }
        return render(request, 'show.html', context)

# ============================================
# Edit Trip
# ============================================

def edit_trip(request, id):
    # verify that there is a user id in session
    # if there is no user id in session, it means no one is properly logged in and should be redirected back to the log/reg page
    if 'user_id' not in request.session:
        errors = User.objects.not_logged_validator()
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:
        # pass forward user based on user_id in session, trip based on id from URL, start and end dates of that trip
        context = {
            'user' : User.objects.get(id=request.session['user_id']),
            'trip' : Trip.objects.get(id=id),
            # .strftime is used to properly format DateTimeField so it can be smoothly passed forward
            # reformatting allows information to autofill the type='date' field in a form
            'start' : Trip.objects.get(id=id).start.strftime("%Y-%m-%d"),
            'end' : Trip.objects.get(id=id).end.strftime("%Y-%m-%d"),
        }
        return render(request, 'edit.html', context)

def update_trip(request, id):
    # verify that this route is being handled after a form submission (i.e. POST route)
    if request.POST:
        # handles errors specifically for trip fields
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors):
           # pass forward 'key' values as 'extra_tags' so jinja can access on the front and access specific errors
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            # redirect back to trip edit page where errors will be rendered with html
            return redirect('/trips/edit/' + str(id))
        else:
            # query for user based on user_id in session
            user = User.objects.get(id=request.session['user_id'])
            # query for trip based on the id passed through the URL
            trip = Trip.objects.get(id=id)

            # override fields based on the inputs from form
            trip.dest=request.POST['dest']
            trip.start=request.POST['start']
            trip.end=request.POST['end']
            trip.plan=request.POST['plan']
            # save trip with updatted fields to database
            trip.save()
            
            # redirect to dashboard where changes should be reflected
            return redirect('/dashboard')

     # if route accessed not on a POST
    else:
        # redirect back to dashboard where nothing should have changed
        return redirect('/dashboard')

# ============================================
# Delete Trip
# ============================================

def delete_trip(request, id):
    trip = Trip.objects.get(id=id)
    trip.delete()

    return redirect('/dashboard')