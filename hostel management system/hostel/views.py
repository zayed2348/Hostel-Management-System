# hostel/views.py
from django.shortcuts import render
from .models import Hostel, Room, Booking, Student
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Student
from django.contrib.auth import authenticate, login as auth_login
from .models import Hostel, Room, Booking, Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hostel, Room, Booking, Student


# views.py

def home(request):
    student = None
    if 'student_id' in request.session:
        try:
            student = Student.objects.get(id=request.session['student_id'])
        except Student.DoesNotExist:
            request.session.flush()  # Clear session if user does not exist
    first_name = student.first_name if student else None
    return render(request, 'hostel/home.html', {'first_name': first_name})


def hostel_list(request):
    hostels = Hostel.objects.all()
    return render(request, 'hostel/hostel_list.html', {'hostels': hostels})

 
def hostel_detail(request, hostel_id):
    hostel = Hostel.objects.get(id=hostel_id)
    rooms = Room.objects.filter(hostel=hostel)
    return render(request, 'hostel/hostel_detail.html', {'hostel': hostel, 'rooms': rooms})

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            student = Student.objects.get(email=email)
            if check_password(password, student.password):
                # You need to manually manage the session as there's no Django built-in user session management for custom models
                request.session['student_id'] = student.id
                return redirect('home')
            else:
                return render(request, 'hostel/login.html', {'error_message': 'Invalid credentials'})
        except Student.DoesNotExist:
            return render(request, 'hostel/login.html', {'error_message': 'Invalid credentials'})
    
    return render(request, 'hostel/login.html')

def user_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            return render(request, 'hostel/register.html', {'error_message': 'Passwords do not match'})

        if Student.objects.filter(email=email).exists():
            return render(request, 'hostel/register.html', {'error_message': 'Email already exists'})

        hashed_password = make_password(password)
        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )

        return redirect('home')

    return render(request, 'hostel/register.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('home')

from django.shortcuts import render, get_object_or_404
from .models import Hostel, Room, Booking
from django.http import HttpResponseRedirect
from django.urls import reverse

def book_room(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)

    if request.method == 'POST':
        room_id = request.POST['room']
        payment_details = request.POST['payment_details']
        
        # You can add more validations here
        # Create a booking record
        Booking.objects.create(
            hostel=hostel,
            room_id=room_id,
            user=request.user,  # Assuming you have user information in request.user
            payment_details=payment_details
        )
        
        # Redirect to a confirmation page or back to the hostel list
        return HttpResponseRedirect(reverse('hostel_list'))
    
    # Get available rooms for this hostel
    rooms = Room.objects.filter(hostel=hostel)
    
    return render(request, 'hostel/book_room.html', {'hostel': hostel, 'rooms': rooms})

# hostel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Hostel, Room, Booking, Student
from .forms import BookingForm

@login_required
def book_room(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user.student
            booking.save()

            # Update the Student model with the booked hostel and room
            student = request.user.student
            student.booked_hostel = hostel
            student.booked_room = booking.room
            student.save()

            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'hostel/book_room.html', {'form': form, 'hostel': hostel})

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'hostel/booking_confirmation.html', {'booking': booking})