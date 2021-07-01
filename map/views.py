from  django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your views here.
 
def show_map(request):
	template_name='map/map.html'
	repairmen = Repairman.objects.all()
	mapbox_access_token = 'pk.eyJ1IjoiYnJhenlrbyIsImEiOiJjazlyY2loNXMwc3M3M2ZydHpkaGVsaDd5In0.N4uOEHtVfwjTxty8zqaTZA'
	context = {
		'repairmen':repairmen,
		'mapbox_access_token':mapbox_access_token,
	}
	return render(request,template_name,context)

class ShowWorkshop(DetailView):
	model = Repairman

	def get(self,request,*args,**kwargs):
		object = get_object_or_404(Repairman, slug=kwargs['slug'])
		mapbox_access_token = 'pk.eyJ1IjoiYnJhenlrbyIsImEiOiJjazlyY2loNXMwc3M3M2ZydHpkaGVsaDd5In0.N4uOEHtVfwjTxty8zqaTZA'
		context = {
			'object':object,
			'mapbox_access_token':mapbox_access_token,
		}
		return render(request,'map/workshopPage.html',context)


class add_rep(CreateView):
	template_name = 'map/add_rep.html'
	model = Repairman
	form_class = RepairmanForm

	def get(self, request, *args, **kwargs):
	    self.object = None
	    form_class = self.get_form_class()
	    form = self.get_form(form_class)
	    service_form = ServicesFormSet()
	    return self.render_to_response(
	        self.get_context_data(form=form,
	                              service_form=service_form))
		  
	def get_context_data(self, **kwargs):
		data = super(add_rep, self).get_context_data(**kwargs)
		if self.request.POST:
			data['services'] = ServicesFormSet(data = self.request.POST)       	
		else:
			data['services'] = ServicesFormSet()
		return data

	def form_valid(self, form):
		all_repairmen = Repairman.objects.all()
		form.instance.user = self.request.user
		context = self.get_context_data()
		services = context['services']
		user = form.instance.user
		if user in all_repairmen:
			messages.error(self.request,'You have already created your worksop!')
			return reverse("map:show_map")
		self.object = form.save()
		if services.is_valid():
			services.instance = self.object
			services.save()
		return super(add_rep, self).form_valid(form)

	def get_success_url(self):
		messages.success(self.request,'Your workwhop has been successfully created!<br> It can now be found on the map!')
		return reverse("map:show_map")