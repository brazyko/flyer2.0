from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_view(request):
	return render(request,"home.html",{})

def about_view( request, *args, **kwargs):
	return render(request,"about.html")


def FAQ_view( request, *args, **kwargs):
	return render(request,"FAQ.html",{})