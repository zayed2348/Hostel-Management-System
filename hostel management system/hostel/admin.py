from django.contrib import admin
from .models import Hostel, Room, Student, Booking

admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Student)
admin.site.register(Booking)