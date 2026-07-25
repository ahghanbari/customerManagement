from django.contrib import admin
from jalali_date import date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_date_jalali', 'machine', 'tools_total', 'cost_total')
    list_filter = ('date', 'machine')
    search_fields = ('name', 'machine', 'problems', 'tools', 'cost')
    @admin.display(description='تاریخ ', ordering='date')
    def get_date_jalali(self, obj):
        return date2jalali(obj.date).strftime('%a, %d %b %Y')