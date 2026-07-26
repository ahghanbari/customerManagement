from django import forms
from jalali_date.fields import JalaliDateField #SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget #AdminSplitJalaliDateTime

from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'date', 'machine', 'problems', 'tools', 'cost', 'image')

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['date'] = JalaliDateField(label='تاریخ', # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget # optional, to use default datepicker
        )