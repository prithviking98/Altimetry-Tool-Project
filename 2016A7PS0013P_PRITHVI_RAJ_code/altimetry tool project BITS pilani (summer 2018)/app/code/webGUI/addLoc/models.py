from django.db import models

# Create your models here.
class Satellite(models.Model):
	nameShort=models.CharField(max_length=5,null=False,unique=True)
	nameLong=models.CharField(max_length=50,null=False,unique=True)
	def __str__(self):
		return str(self.nameLong)

class Country(models.Model):
	name=models.CharField(max_length=50,null=False,unique=True)
	def __str__(self):
		return str(self.name)

class State(models.Model):
	name=models.CharField(max_length=20,null=False,unique=True)
	def __str__(self):
		return str(self.name)

class WaterBodyType(models.Model):
	name=models.CharField(max_length=20,null=False,unique=True)
	def __str__(self):
		return str(self.name)

class Basin(models.Model):
	name=models.CharField(max_length=60,null=False,unique=True)
	def __str__(self):
		return str(self.name)

class Location(models.Model):
	latitude=models.FloatField(null=False)
	longitude=models.FloatField(null=False)
	satellite=models.ForeignKey(Satellite,on_delete=models.CASCADE,null=False,default=1)
	name=models.CharField(max_length=100,null=False)
	state=models.ForeignKey(State,default=1,null=False,on_delete=models.CASCADE)
	country=models.ForeignKey(Country,default=1,null=False,on_delete=models.CASCADE)
	waterBodyType=models.ForeignKey(WaterBodyType,default=1,null=False,on_delete=models.CASCADE)
	basin=models.ForeignKey(Basin,null=True,blank=True,on_delete=models.CASCADE)
	class Meta:
		unique_together=('latitude','longitude')
	def __str__(self):
		s=str(self.name)+' '+str(self.waterBodyType)+' '+str(self.latitude)+' '+str(self.longitude) 
		return s

class ElevationGeoid(models.Model):
	elevation=models.FloatField(null=False)
	date=models.DateField(null=False)
	location=models.ForeignKey(Location,on_delete=models.CASCADE)
	class Meta:
		unique_together=('date','location')
	def getEl(self):
		return float(self.elevation)
	def __str__(self):
		return str(self.elevation)+' '+str(self.location)

class ElevationMss(models.Model):
	elevation=models.FloatField(null=False)
	date=models.DateField(null=False)
	location=models.ForeignKey(Location,on_delete=models.CASCADE,null=False)
	class Meta:
		unique_together=('date','location')
	def getEl(self):
		return float(self.elevation)
	def __str__(self):
		return str(self.elevation)+' '+str(self.location)

class Kmz(models.Model):
	file=models.FileField(upload_to='kmz/', null=True)