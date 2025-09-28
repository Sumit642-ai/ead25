from django.db import models

# Create your models here.
class EADCities(models.Model):
    city=models.CharField(max_length=30)
    def __str__(self):
        return self.city
class EADVenue(models.Model):
    city=models.ForeignKey(EADCities,on_delete=models.CASCADE)
    venue=models.CharField(max_length=30)
    date=models.DateField()
    maintopic=models.CharField(max_length=50)
    image=models.ImageField(null=False,upload_to='static/images')
    def __str__(self):
        return self.city.city

class EADSpeakers(models.Model):
    city=models.ForeignKey(EADCities,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    designition=models.CharField(max_length=50)
    linkedin=models.URLField(max_length=200)
    photo=models.ImageField(upload_to="EAD/images")
    def __str__(self):
        return self.city.city +'EAD ' + self.name

class LSMCities(models.Model):
    city=models.CharField(max_length=30)
    def __str__(self):
        return self.city


class LSMVenue(models.Model):
    city=models.ForeignKey(LSMCities,on_delete=models.CASCADE)
    venue=models.CharField(max_length=30)
    date=models.DateField()
    maintopic=models.CharField(max_length=50)
    image=models.ImageField(null=False,upload_to='static/images')
    def __str__(self):
        return self.city.city


class LSMSpeakers(models.Model):
    city=models.ForeignKey(LSMCities,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    designition=models.CharField(max_length=50)
    linkedin=models.URLField(max_length=200)
    photo=models.ImageField(upload_to="EAD/images")
    def __str__(self):
        return self.city.city +' LSM ' + self.name






