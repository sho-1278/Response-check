from django.contrib import admin
from django.urls import path, include
from rpspgate.views import *

urlpatterns = [
	path('index', index, name="index"),	
	path('results', results, name="results"),
	path('errors', errors, name="errors")
]