from  django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic import ListView, FormView,View
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
# Create your views here.
def show_all_users(request):
	users = User.objects.all()
	context = {
		'users':users,
	}
	return render(request,'users/show_all_users.html',context)
@login_required
def show_user_profile(request,user_slug):
	users = User.objects.all()
	slug = user_slug
	users = users.filter(username = slug)
	owner = users[0]
	user_products = Product.objects.all()
	user_products = user_products.filter(Q(author = owner))
	context = {
		'user_products':user_products,
		'owner':owner,
	}
	return render(request,'users/show_user_profile.html',context)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, '{username},your account has bees successfully created! Please log in now')
			return redirect('login')
	else:
		form = UserRegisterForm()
	context ={
		'form':form
	}
	return render(request,'users/register.html',context)


@login_required
def profile(request):
	user = request.user
	all_products = Product.objects.all()
	user_products = all_products.filter(Q(author = user))
	liked_products = all_products.filter(Q(users_like = user))
	context = {
		'liked_products':liked_products,
		'user_products':user_products,
		'all_products':all_products,
	}

	return render(request,'users/profile.html',context)


@login_required
def profile_update(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {
		'u_form':u_form,
		'p_form':p_form,
	}

	return render(request,'users/profile_update.html',context)


