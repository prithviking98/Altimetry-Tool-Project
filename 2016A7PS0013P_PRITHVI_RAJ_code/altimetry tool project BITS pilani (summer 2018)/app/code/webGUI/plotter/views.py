from django.shortcuts import render
from addLoc.models import *
from django.contrib import messages
import datetime
import numpy as np 


# Create your views here.

def home(request):
	context={}
	if request.method=='POST':
		results=Location.objects.all()
		keys=request.POST.keys()
		if 'name' in keys and request.POST['name'] != "":
			results=results.filter(name=request.POST['name'])
		if 'basin' in keys and request.POST['basin']!='':
			results=results.filter(basin__id=int(request.POST['basin']))
		if 'wbt' in keys and request.POST['wbt']!='':
			results=results.filter(waterBodyType__id=int(request.POST['wbt']))
		if 'satellite' in keys and request.POST['satellite']!='':
			results=results.filter(satellite__id=int(request.POST['satellite']))
		if 'state' in keys and request.POST['state']!='':
			results=results.filter(state__id=int(request.POST['state']))
		if len(results)==0:
			messages.error(request, 'Sorry there are no points satisfying your search conditions.')
		else:
			messages.info(request, 'Found {} points that match your search condition. Click the Zoom to Points button on the right to zoom to those points.'.format(len(results)))
			context={'results':results}
	added_locs=Location.objects.all();
	names=[]
	for loc in added_locs:
		names.append(str(loc.name))
	states=State.objects.order_by('name');
	countries=Country.objects.order_by('name');
	basins=Basin.objects.order_by('name');
	sats=Satellite.objects.order_by('nameLong');
	wbt=WaterBodyType.objects.order_by('name');
	context.update({'added_locs':added_locs,'names':names, 'states':states, 'countries':countries,
	'basins':basins, 'sats':sats, 'wbt':wbt})
	return render(request,'plotter/home.html',context)

def plotMss(request,loc_id):
	context={}
	loc=Location.objects.get(pk=loc_id)
	results=ElevationMss.objects.filter(location__id=int(loc_id)).order_by('date')
	
	context={'results':results,'loc':loc}
	return render(request,'plotter/plotMss.html',context)

def plotGeoid(request,loc_id):
	context={}
	loc=Location.objects.get(pk=loc_id)
	results=ElevationGeoid.objects.filter(location__id=int(loc_id)).order_by('date')
	
	context={'results':results,'loc':loc}
	return render(request,'plotter/plotGeoid.html',context)	

