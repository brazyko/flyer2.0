from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product,Category
from blog.models import Article, Category


# Create your views here.
def home_view(request):
	products = Product.objects.all().order_by('-publish')[0:5]
	articles = Article.objects.all().order_by('-publish')[0:5]
	context = {
		'products':products,
		'articles':articles,
	}
	return render(request,"home.html",context)

def about_view( request, *args, **kwargs):
	return render(request,"about.html")


def FAQ_view( request, *args, **kwargs):
	return render(request,"FAQ.html",{})