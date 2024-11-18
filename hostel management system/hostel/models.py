# hostel/models.py
from django.db import models

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    image_url = models.URLField(max_length=200, default="https://example.com/default-hostel-image.jpg")

    def __str__(self):
        return self.name

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Add this line
    booked_hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True, blank=True)
    booked_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Booking(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_details = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.student} - {self.room}"
