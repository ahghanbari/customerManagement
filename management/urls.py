from django.urls import path

from . import views

urlpatterns = [
    path('', views.CustomerListView, name='customer_list'),
]