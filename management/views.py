from django.shortcuts import render
from .models import Customer

from jalali_date import date2jalali


def CustomerListView(request):
    
    customers = Customer.objects.all()
    for customer in customers:
        customer.jalali_date = date2jalali(customer.date)
    return render(request, 'management/customer_list.html', {'customers': customers})