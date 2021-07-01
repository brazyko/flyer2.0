from django.urls import path,include
from .views import (
		ArticleCreateView,
		ArticleDetailView,
		ArticleListView,
		ArticleDeleteView,
		ArticleUpdateView,
		search,
      postsByCategory,
      UpdateCommentVote,
	)


app_name= 'articles'
urlpatterns = [
   path('', ArticleListView, name='article-list'),
   path('create/', ArticleCreateView,name='article-create'),
   path('category-<postcategoryslug>',postsByCategory,name='posts-by-category'),
   path('<slug>/', ArticleDetailView, name='article-detail'),
   path('search',search,name='search'),
   path('<slug>/update/',ArticleUpdateView.as_view(), name='article-update'),   
   path('<slug>/delete/',ArticleDeleteView.as_view(), name='article-delete'),
   path('tinymce/', include('tinymce.urls')),
   path('<article_slug>/<int:comment_id>/<str:opition>', UpdateCommentVote.as_view(), name='requirement_comment_vote'),
]

