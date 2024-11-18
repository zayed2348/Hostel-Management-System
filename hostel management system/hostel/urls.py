# hostel/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hostels/', views.hostel_list, name='hostel_list'),
    path('hostels/<int:hostel_id>/', views.hostel_detail, name='hostel_detail'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='register'),  # Add this line
    path('logout/', views.user_logout, name='user_logout'),  # Added logout URL
    path('book/<int:hostel_id>/', views.book_room, name='book_room'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
]