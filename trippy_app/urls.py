from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('trips/new', views.create_trip),
    path('new_trip', views.new_trip),
    path('trips/<int:id>', views.show_trip),
    path('trips/edit/<int:id>', views.edit_trip),
    path('update_trip/<int:id>', views.update_trip),
    path('trips/delete/<int:id>', views.delete_trip),
]