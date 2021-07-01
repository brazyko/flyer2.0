from django import forms
from .models import *
from django.forms.models import inlineformset_factory

class RepairmanForm(forms.ModelForm):
	class Meta:
		model = Repairman
		fields=[
		'main_image',
		'workshop_name',
		'about_workshop',
		'address',
		'coord_h',
		'coord_v',
		]
		

ServicesFormSet = inlineformset_factory(Repairman, Services, fields= ['name','description','price'], can_delete=True,extra=80,max_num=80 )


