from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class Client(AbstractUser):
	username = models.CharField(max_length=255,unique=True)
	password = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	full_name = models.CharField(max_length=255)

class Language(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name

class Book(models.Model):
	name = models.CharField(max_length=255)
	file = models.FileField(upload_to="book/files/")
	lang = models.ForeignKey(Language,on_delete=models.CASCADE)
	auth = models.ForeignKey(Client,on_delete=models.CASCADE)
	img = models.ImageField(upload_to="book/image/")
	date = models.DateTimeField()
	reyting = models.IntegerField(default=0)
	reyting_count = models.IntegerField(default=0)
	text = models.TextField()
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	def __str__(self):
		return self.name

class ReytingBook(models.Model):
	book = models.ForeignKey(Book,on_delete=models.CASCADE)
	auth = models.ForeignKey(Client,on_delete=models.CASCADE)
	star = models.IntegerField()
	def __str__(self):
		return str(self.star)


class AudioBook(models.Model):
	name = models.CharField(max_length=255)
	file = models.FileField(upload_to="book/files/audio/")
	lang = models.ForeignKey(Language,on_delete=models.CASCADE)
	auth = models.ForeignKey(Client,on_delete=models.CASCADE)
	img = models.ImageField(upload_to="book/image/")
	date = models.DateTimeField()
	reyting = models.IntegerField(default=0)
	reyting_count = models.IntegerField(default=0)
	text = models.TextField()
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	def __str__(self):
		return self.name

class ReytingAudioBook(models.Model):
	book = models.ForeignKey(AudioBook,on_delete=models.CASCADE)
	auth = models.ForeignKey(Client,on_delete=models.CASCADE)
	star = models.IntegerField()
	def __str__(self):
		return str(self.star)


class HistoryAudioBook(models.Model):
	types = models.IntegerField(choices=((1,"going to"),(2,"reading"),(3,"readed")))
	book = models.ForeignKey(AudioBook,on_delete=models.CASCADE)
	user = models.ForeignKey(Client,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

class HistoryBook(models.Model):
	types = models.IntegerField(choices=((1,"going to"),(2,"reading"),(3,"readed")))
	book = models.ForeignKey(Book,on_delete=models.CASCADE)
	user = models.ForeignKey(Client,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

