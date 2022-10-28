from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default-user-image.png', upload_to='profile_pics')
	about_me = models.CharField(max_length=150, blank=True, null=True)
	instagram = models.CharField(max_length=25, blank=True, null=True)
	youtube = models.CharField(max_length=25, blank=True, null=True)
	twitter = models.CharField(max_length=25, blank=True, null=True)

	def __str__(self):
		return '{} Profile '.format(self.user.username)

