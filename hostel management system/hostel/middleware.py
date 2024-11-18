from django.shortcuts import redirect
from .models import Student

class StudentAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'student_id' in request.session:
            try:
                request.student = Student.objects.get(id=request.session['student_id'])
            except Student.DoesNotExist:
                del request.session['student_id']
                request.student = None
        else:
            request.student = None
        
        response = self.get_response(request)
        return response
