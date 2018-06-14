from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response

def permission_denied(request):
    return render_to_response("403.html")

def page_not_found(request):
    return render_to_response("404.html")

def page_error(request):
    return render_to_response("500.html")
