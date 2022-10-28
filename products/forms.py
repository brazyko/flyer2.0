
from .models import *

from django import forms

from django.forms.models import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from mptt.forms import TreeNodeChoiceField



class RawProductForm(forms.ModelForm):
	class Meta:
		model = ProductImage
		photo = forms.ImageField()
		fields = [
			'title',
			'category',
			'description',
			'summary',
			'features',
			'price',

		]
	title =		  forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Your title"}))
	category = TreeNodeChoiceField(queryset=Category.objects.all(),level_indicator=mark_safe("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),label=_("Categories"))
	description = forms.CharField(
			widget = forms.Textarea(
					attrs={
						"placeholder":"Your description",
						"class":"new-class-name two",
						"id":"my_id_for_text_area",
						"rows":10,
						"cols":60,
					}
				)
		)
	main_image = forms.ImageField()
	summary = forms.CharField(
		widget= forms.Textarea(
					attrs={
						"placeholder":"summary",
						"rows":5,
						"cols":120,
					}
				)

			
		)
	features = forms.BooleanField()
	price =    forms.DecimalField()

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = [
			'title',
			'category',
			'description',
			'summary',
			'city',
			'features',
			'price',
		]
	category = TreeNodeChoiceField(queryset=Category.objects.all(),level_indicator=mark_safe("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),label=_("Categories"))

	

ImageFormSet = inlineformset_factory(Product, ProductImage, fields= ['image'], can_delete=True,extra=8,max_num=8 )


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentProduct
        fields =['body']