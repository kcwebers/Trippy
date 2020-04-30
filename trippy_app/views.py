from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


# ============================================
# Login/Registration
# ============================================

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.POST:
        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )

            request.session['user_id'] = user.id
            return redirect('/dashboard')

def login(request):
    if request.POST:
        errors = User.objects.log_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        else:
            user = User.objects.get(email=request.POST['email_input'])
            request.session['user_id'] = user.id
            return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

# ============================================
# Dashboard
# ============================================

def dashboard(request):
    if 'user_id' not in request.session:
        errors = User.objects.not_logged_validator()
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        context = {
            'user' : user,
            'trips' : Trip.objects.all()
        }
        return render(request, 'dashboard.html', context)

# ============================================
# Create Trip
# ============================================

def create_trip(request):
    if 'user_id' not in request.session:
        errors = User.objects.not_logged_validator()
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        context = {
            'user' : user
        }
        return render(request, 'create.html', context)

def new_trip(request):
    if request.POST:
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/trips/new')
        else:
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)

            trip = Trip.objects.create(
                dest=request.POST['dest'],
                start=request.POST['start'],
                end=request.POST['end'],
                plan=request.POST['plan'],
                creator=user
            )

            return redirect('/dashboard')

# ============================================
# Show Trip
# ============================================

def show_trip(request, id):
    if 'user_id' not in request.session:
        errors = User.objects.not_logged_validator()
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        context = {
            'user' : user,
            'trip' : Trip.objects.get(id=id)
        }
        return render(request, 'show.html', context)

# ============================================
# Edit Trip
# ============================================

def edit_trip(request, id):
    if 'user_id' not in request.session:
        errors = User.objects.not_logged_validator()
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:

        context = {
            'user' : User.objects.get(id=request.session['user_id']),
            'trip' : Trip.objects.get(id=id),
            'start' : Trip.objects.get(id=id).start.strftime("%Y-%m-%d"),
            'end' : Trip.objects.get(id=id).end.strftime("%Y-%m-%d"),
        }
        return render(request, 'edit.html', context)

def update_trip(request, id):
    if request.POST:
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/trips/edit/' + str(id))
        else:
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)

            trip = Trip.objects.get(id=id)

            trip.dest=request.POST['dest']
            trip.start=request.POST['start']
            trip.end=request.POST['end']
            trip.plan=request.POST['plan']
            trip.save()
            
            return redirect('/dashboard')

# ============================================
# Delete Trip
# ============================================

def delete_trip(request, id):
    trip = Trip.objects.get(id=id)
    trip.delete()

    return redirect('/dashboard')