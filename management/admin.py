from django.contrib import admin
from jalali_date import date2jalali
from jalali_date.admin import ModelAdminJalaliMixin
from django.utils.safestring import mark_safe
from django.urls import reverse
 
from .models import Customer
from .forms import CustomerForm

@admin.register(Customer)
class CustomerAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('get_name', 'get_date_jalali', 'get_day_of_week', 'machine', 'get_debt','get_tools_total', 'get_partner_fee', 'get_cost_total', 'get_total', 'get_report_link')
    list_filter = ('date', 'debt')
    search_fields = ('name', 'machine', 'problems', 'address', 'tools', 'cost')
    form = CustomerForm

    @admin.display(description='تاریخ ', ordering='date')
    def get_date_jalali(self, obj):
        return date2jalali(obj.date).strftime('%Y/%m/%d %B')

    @admin.display(description='روز هفته', ordering='date')
    def get_day_of_week(self, obj):
        weekdays = {
            2: 'دوشنبه',
            3: 'سه‌شنبه',
            4: 'چهارشنبه',
            5: 'پنج‌شنبه',
            6: 'جمعه',
            0: 'شنبه',
            1: 'یک‌شنبه',
        }
        return weekdays.get(date2jalali(obj.date).weekday())
    
    def multiply_by_million(self, value):
        if value and value.replace('.', '').isdigit():
            try:
                if len(value) == 3 and(value.find('.') == -1):
                    return int(float(value) * 1000)
                return int(float(value) * 1000000)
            except (ValueError, TypeError):
                return 0
        return 0

    @admin.display(description='نام مشتری', ordering='name')
    def get_name(self, obj):
        return obj.name

    @admin.display(description='بدهی مشتری', ordering='debt')
    def get_debt(self, obj):
        if obj.debt is not None:
            debt = self.multiply_by_million(obj.debt)
            return f"{debt:,} تومان"
        return "0 تومان"
    
    @admin.display(description='سهم همکار', ordering='partner_fee')
    def get_partner_fee(self, obj):
        if obj.partner_fee is not None:
            fee = self.multiply_by_million(obj.partner_fee)
            return f"{fee:,} تومان"
        return "0 تومان"

    @admin.display(description='هزینه قطعات', ordering='tools_total')
    def get_tools_total(self, obj):
        if obj.tools_total is not None:
            return f"{obj.tools_total:,} تومان"
        return "0 تومان"
    
    @admin.display(description='هزینه اجرت', ordering='cost_total')
    def get_cost_total(self, obj):
        if obj.cost_total is not None:
            return f"{obj.cost_total:,} تومان"
        return "0 تومان"

    @admin.display(description='جمع کل', ordering='total')
    def get_total(self, obj):
        if obj.total is not None:
            return f"{obj.total:,} تومان"
        return "0 تومان"

    @admin.display(description='لینک گزارش', ordering='date')
    def get_report_link(self, obj):
        url = reverse('management:report_list')
        return mark_safe(f'<a href="{url}">گزارش درآمد</a>')