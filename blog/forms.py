from django import forms

from .models import Article,Comment

class ArticleModelForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = [
			'title',
			'categories',
			'description',
			'image',
			'featured',
		]

class CommentForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={
		'class':'form-control',
		'placeholder':'Залишити коментар',
		'rows':'4',
		}))
	class Meta:
		model = Comment
		fields = ('content','parent')
			