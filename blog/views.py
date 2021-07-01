from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.db.models import Count,Q
from django.views.generic import (
	CreateView,
	DetailView,
	ListView,
	UpdateView,
	DeleteView,
	)
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Article,Category,DisLike,Like,Comment
from .forms import ArticleModelForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def get_category_count():
	queryset = Article.objects.values('categories__name').annotate(Count('categories__name'))
	return queryset


def ArticleCreateView(request):
	form = ArticleModelForm(request.POST, request.FILES)
	if form.is_valid():
		form = form.save(commit=False)
		form.author = request.user
		form.save()
		return redirect("../")
		
	else:
		form = ArticleModelForm(request.POST, request.FILES)
	template = 'articles/article_create.html'
	context = {
		'form':form,
	}
	return render(request,template, context)

def ArticleListView(request):
	categories = Category.objects.all()
	posts = Article.objects.all()
	posts = posts.order_by('-publish') 
	latest  = Article.objects.order_by('-publish')[0:3]
	top_posts  = Article.objects.order_by('-view_count')[0:3]
	top_categories  = Category.objects.all()
	top_categories.order_by()[0:3]
	page_number = request.GET.get('page',1)
	paginator = Paginator(posts,6)
	page_obj = paginator.get_page(page_number)
	try:
		posts = paginator.page(page_number)
	except PageNotAnInteger:
	    posts = paginator.page(1)
	except EmptyPage:
	    posts = paginator.page(paginator.num_pages)
	context = {
		'posts':posts,
		'page_obj':page_obj,
		'latest_posts':latest,
		'top_posts':top_posts,
		'top_categories':top_categories,
		'categories':categories,
	}
	return render(request, 'articles/blog.html',context)

def search(request):
	queryset = Article.objects.all()
	query = request.GET.get('q')
	categories = Category.objects.all()
	if query:
		posts = queryset.filter(
			Q(title__icontains=query)
		).distinct()
	posts = posts.order_by('-publish') 
	latest  = Article.objects.order_by('-publish')[0:3]
	top_posts  = Article.objects.order_by('-view_count')[0:3]
	top_categories  = Category.objects.all()
	top_categories.order_by()
	page_number = request.GET.get('page',1)
	paginator = Paginator(posts,6)
	page_obj = paginator.get_page(page_number)
	try:
		posts = paginator.page(page_number)
	except PageNotAnInteger:
	    posts = paginator.page(1)
	except EmptyPage:
	    posts = paginator.page(paginator.num_pages)
	context = {
		'posts':posts,
		'search_data':query,
		'page_obj':page_obj,
		'latest_posts':latest,
		'top_posts':top_posts,
		'top_categories':top_categories,
		'categories':categories,
	}
	return render(request, 'search_result.html', context)


def ArticleDetailView(request, slug):
	categories = Category.objects.all()
	top_categories = categories.order_by()[0:3]
	latest  = Article.objects.order_by('-publish')[0:3]
	post = get_object_or_404(Article,slug=slug)
	post.view_count = post.view_count + 1
	top_posts  = Article.objects.order_by('-view_count')[0:3]
	post.save()
	form = CommentForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.instance.user = request.user
			form.instance.post = post
			form.save()
			return redirect("/blog/"+post.slug)
	context ={
		'form':form,
		'top_posts':top_posts,
		'post':post,
		'latest_posts':latest,
		'top_categories':top_categories,
	}
	return render(request,'articles/article_detail.html',context)

class ArticleUpdateView(UpdateView):
	template_name = 'articles/article_create.html'
	form_class = ArticleModelForm
	queryset = Article.objects.all() 

	def get_object(self):
		slug = self.kwargs.get("slug")
		return get_object_or_404(Article,slug=slug)

	def form_valid(self,form):
		print(form.cleaned_data)
		return super().form_valid(form)

	def get_success_url(self):
		return '../'

class ArticleDeleteView(DeleteView):
	template_name = 'articles/article_delete.html'

	def get_object(self):
		slug = self.kwargs.get("slug")
		return get_object_or_404(Article, slug=slug)

	def get_success_url(self):
		return reverse("articles:article-list")


def postsByCategory(request,postcategoryslug):
	categories = Category.objects.all()
	slug = postcategoryslug
	current_category = Category.objects.get(slug = slug)
	posts = current_category.posts.all()
	posts = posts.order_by('-publish') 
	latest  = Article.objects.order_by('-publish')[0:3]
	top_posts  = Article.objects.order_by('-view_count')[0:3]
	top_categories  = Category.objects.all()
	top_categories.order_by()
	page_number = request.GET.get('page',1)
	paginator = Paginator(posts,6)
	page_obj = paginator.get_page(page_number)
	try:
		posts = paginator.page(page_number)
	except PageNotAnInteger:
	    posts = paginator.page(1)
	except EmptyPage:
	    posts = paginator.page(paginator.num_pages)
	context = {
		'posts':posts,
		'current_category':current_category,
		'page_obj':page_obj,
		'latest_posts':latest,
		'top_posts':top_posts,
		'top_categories':top_categories,
		'categories':categories,
	}
	return render(request,'articles/postsBycategory.html',context)



class UpdateCommentVote(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):

        article_slug = self.kwargs.get('article_slug',None)
        post = Article.objects.get(slug=article_slug)

        id = self.kwargs.get('comment_id', None)
        opition = self.kwargs.get('opition', None) # like or dislike button clicked

        comment = get_object_or_404(Comment, id=id)

        try:
            # If child DisLike model doesnot exit then create
            comment.dis_likes
        except Comment.dis_likes.RelatedObjectDoesNotExist as identifier:
            DisLike.objects.create(comment = comment)

        try:
            # If child Like model doesnot exit then create
            comment.likes
        except Comment.likes.RelatedObjectDoesNotExist as identifier:
        	Like.objects.create(comment = comment)

        if opition.lower() == 'like':

            if request.user in comment.likes.users.all():
                comment.likes.users.remove(request.user)
            else:    
                comment.likes.users.add(request.user)
                comment.dis_likes.users.remove(request.user)

        elif opition.lower() == 'dis_like':

            if request.user in comment.dis_likes.users.all():
                comment.dis_likes.users.remove(request.user)
            else:    
                comment.dis_likes.users.add(request.user)
                comment.likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(reverse('articles:article-detail',args=[post.get_absolute_url()]))
        return HttpResponseRedirect(reverse('articles:article-detail',args=[post.get_absolute_url()]))