from django.urls import path

from . import views

app_name='addLoc'
urlpatterns = [
	# path('upload/', views.upload, name='upload'),
	path('',views.home,name='home')
]