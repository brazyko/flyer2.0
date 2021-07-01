from  django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Category
from .forms import *
from django.urls import reverse
from django.views.generic import ListView, FormView,RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q ,F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,HttpResponseRedirect, HttpResponseNotFound,Http404,JsonResponse
from mptt.forms import MoveNodeForm
# Create your views here.
from django.db import transaction
from django.urls import reverse_lazy

def ProductList(request):
	products = Product.objects.all()
	products = products.order_by('-publish')
	categories = Category.objects.all()
	search = request.GET.get('q')
	selected = request.GET.get('select')
	sort = request.GET.get('sort')
	if selected == 'full':
		products = products.filter(Q(title = search))
	elif selected == 'contains':
		products = products.filter(Q(title__icontains = search))
	if sort == 'lowhigh':
		products = products.order_by('price')
	elif sort == 'highlow':
		products = products.order_by('-price')
	elif sort == 'not':
		products = products
	page_number = request.GET.get('page',1)
	paginator = Paginator(products,12)
	page_obj = paginator.get_page(page_number)
	try:
		products = paginator.page(page_number)
	except PageNotAnInteger:
	    products = paginator.page(1)
	except EmptyPage:
	    products = paginator.page(paginator.num_pages)
	context = {
		'products':products,
		'categories':categories,
		'page_obj': page_obj,
		'q':search,
		'select':selected,
		'sort':sort,
	}
	template = 'products/product_list.html'
	return render(request, template ,context)

class product_detail_view(DetailView):
    def get(self, request, *args, **kwargs):
	    object = get_object_or_404(Product, slug=kwargs['prodcut_slug'])
	    comments = object.comments.filter(active=True)
	    new_comment = None
	    # Comment posted
	    if request.method == 'POST':
	        comment_form = CommentForm(data=request.POST)
	        if comment_form.is_valid():
	            new_comment = comment_form.save(commit=False)
	            new_comment.product = object
	            new_comment.save()
	    else:
	        comment_form = CommentForm()
	    context = {
	    'object': object,
	    'comments': comments,
	    'comment_form': comment_form,
	    }
	    return render(request, 'products/product_detail.html', context)



class ProductLikeToggle(RedirectView):
    def get_redirect_url(self,*args,**kwargs):
    	slug = self.kwargs.get('prodcut_slug')
    	obj = get_object_or_404(Product, slug=slug)
    	url_ =obj.get_absolute_url()
    	user = self.request.user
    	if user.is_authenticated:
    		if user in obj.users_like.all():
    			obj.users_like.remove(user)
    		else:
    			obj.users_like.add(user)
    	return url_

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class ProductLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,category_slug=None,prodcut_slug=None, format=None):
        slug = self.kwargs.get('prodcut_slug')
        obj = get_object_or_404(Product, slug=slug)
        url_ =obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked  = False
        if user.is_authenticated:
        	if user in obj.users_like.all():
        		liked = False
        		obj.users_like.remove(user)		
        	else:
        		liked = True
        		obj.users_like.add(user)
        	updated = True
        	data = {
        	"updated":updated,
        	"liked":liked,
        }
        return Response(data)



class product_create_view(CreateView):
	template_name = 'products/product_create.html'
	model = Product
	form_class = ProductForm

	def get(self, request, *args, **kwargs):
	    self.object = None
	    form_class = self.get_form_class()
	    form = self.get_form(form_class)
	    image_form = ImageFormSet()
	    return self.render_to_response(
	        self.get_context_data(form=form,
	                              image_form=image_form))

	def get_context_data(self, **kwargs):
	        data = super(product_create_view, self).get_context_data(**kwargs)
	        if self.request.POST:
	            data['images'] = ImageFormSet(data = self.request.POST,files=self.request.FILES)       	
	        else:
	            data['images'] = ImageFormSet()
	        return data

	def form_valid(self, form):
	    context = self.get_context_data()
	    images = context['images']
	    with transaction.atomic():
	        form.instance.author = self.request.user
	        self.object = form.save()
	        if images.is_valid():
	            images.instance = self.object
	            images.save()
	    return super(product_create_view, self).form_valid(form)

	def get_success_url(self):
		messages.success(self.request,'Your item has been successfully added!')
		return reverse("products:product-list1")

class product_update_view(UpdateView):
    template_name = 'products/product_create.html'
    form_class = ProductForm
    queryset = Product.objects.all() 
	
    def get_object(self):
    	slug = self.kwargs.get("prodcut_slug")
    	return get_object_or_404(Product,slug=slug)

    def get_context_data(self, **kwargs):
        data = super(product_update_view, self).get_context_data(**kwargs)
        if self.request.POST:
            data['image_form'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['image_form'] = ImageFormSet(instance=self.object)
        return data	

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['image_form']
        with transaction.atomic():
        	self.object = form.save(commit=False)
	        if images.is_valid():
	            images.instance = self.object
	            images.save()
        return super(product_update_view, self).form_valid(form)


    def get_success_url(self):
    	messages.success(self.request,'Your item has been successfully updated!')
    	return reverse("products:product-list1")

class product_delete_view(DeleteView):
	template_name= 'products/product_delete.html'

	def get_object(self):
		slug = self.kwargs.get("prodcut_slug")
		return get_object_or_404(Product, slug=slug)

	def get_success_url(self):
		messages.success(self.request,'Your item has beed deleted')
		return reverse("products:product-list1")

def products_by_category(request,category_slug):
	categories = Category.objects.all()
	slug = category_slug
	current_category = Category.objects.get(slug = slug)
	children = current_category.get_children()
	ancestors = current_category.get_ancestors()
	products = current_category.products.all()
	categories = Category.objects.get(slug = slug).get_descendants(include_self=True)
	for category in categories.all():
		products |= category.products.all()
	if not products:
		return redirect('products:product-list1')
	page_number = request.GET.get('page',1)
	paginator = Paginator(products,12)
	page_obj = paginator.get_page(page_number)
	try:
		products = paginator.page(page_number)
	except PageNotAnInteger:
	    products = paginator.page(1)
	except EmptyPage:
	    products = paginator.page(paginator.num_pages)
	context = {
		'categories':categories,
		'current_category':current_category,
		'children':children,
		'ancestors':ancestors,
		'products':products,
		'page_obj':page_obj,
	}
	template = 'products/products_by_category_list.html'
	return render(request,template,context)

