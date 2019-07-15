from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import *
from django.db import IntegrityError
from django.contrib import messages
# Create your views here.

'''
def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        kmzfile = Kmz()
        kmzfile.file.save('file.kmz', myfile)
        return render(request, 'addLoc/upload.html',)
    return render(request, 'addLoc/upload.html')
'''

def home(request):
	if request.method=='POST' and request.POST['basin']!='':
		location= Location(
			latitude=float(request.POST['latitude']),
			longitude=float(request.POST['longitude']),
			satellite=Satellite.objects.get(pk=request.POST['satellite']),
			name=request.POST['name'],
			state=State.objects.get(pk=request.POST['state']),
			country=Country.objects.get(pk=request.POST['country']),
			waterBodyType=WaterBodyType.objects.get(pk=request.POST['wbt']),
			basin=Basin.objects.get(pk=request.POST['basin'])
			)
		try:
			location.save()
			messages.success(request, "Location added successfully! (you can see a new point at added location)")
		except IntegrityError:
			messages.error(request, 'Sorry point with exact same coordinates already exists. Please select another point.')
	elif request.method=='POST' and request.POST['basin']=='':
		location= Location(
			latitude=float(request.POST['latitude']),
			longitude=float(request.POST['longitude']),
			satellite=Satellite.objects.get(pk=request.POST['satellite']),
			name=request.POST['name'],
			state=State.objects.get(pk=request.POST['state']),
			country=Country.objects.get(pk=request.POST['country']),
			waterBodyType=WaterBodyType.objects.get(pk=request.POST['wbt']),
			)
		try:
			location.save()
			messages.success(request, "Location added successfully! (you can see a new point at added location)")
		except IntegrityError:
			messages.error(request, 'Sorry point with exact same coordinates already exists. Please select another point.')
	added_locs=Location.objects.all();
	states=State.objects.order_by('name');
	countries=Country.objects.order_by('name');
	basins=Basin.objects.order_by('name');
	sats=Satellite.objects.order_by('nameLong');
	wbt=WaterBodyType.objects.order_by('name');
	context={'added_locs':added_locs, 'states':states, 'countries':countries,
	'basins':basins, 'sats':sats, 'wbt':wbt}
	return render(request,'addLoc/home.html',context)

