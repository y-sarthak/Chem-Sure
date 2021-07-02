from django.db import models

# Create your models here.

class Chem(models.Model):
	image = models.ImageField(upload_to='images/')


	def __str__(self):
		return self.Name



	def get_absolute_url(self):
		return reverse("img:employee_update",kwargs={'id':self.id}) 