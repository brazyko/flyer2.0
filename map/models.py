from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.text import slugify

# Create your models here.

class Repairman(models.Model):
	workshop_name	= models.CharField(max_length=50)
	slug            = models.SlugField(unique=True)
	user     		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	main_image      = models.ImageField(null=True,upload_to = 'images/%Y/%m/%d/%H/%M/%S/',)
	address			= models.CharField(max_length=150,null=True)
	about_workshop 	= models.CharField(max_length=200)
	coord_v   		= models.FloatField()
	coord_h    		= models.FloatField(blank=True)

	def __unicode__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.workshop_name)
		
		super(Repairman, self).save(*args, **kwargs)

	def __str__(self):
		return self.workshop_name

class Services(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	price       = models.IntegerField()
	repairman = models.ForeignKey('Repairman',on_delete=models.CASCADE,related_name='services')

	def __str__(self):
		return self.repairman.workshop_name