from django.urls import path

from . import views

app_name='plotter'
urlpatterns = [
	path('',views.home,name='home'),
	path('<int:loc_id>/plotMss/',views.plotMss,name='plotMss'),
	path('<int:loc_id>/plotGeoid/',views.plotGeoid,name='plotGeoid')
]