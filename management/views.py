from django.shortcuts import render
from jalali_date import date2jalali
from django.utils.encoding import force_str
from django.db import models
from jdatetime import datetime as jalali_datetime
from django.contrib.auth.decorators import login_required

from .models import Customer


@login_required
def ReportListView(request):
    def multiply_by_million(value):
        try:
            if len(value) == 3 and(value.find('.') == -1):
                return int(float(value) * 1000)
            return int(float(value) * 1000000)
        except (ValueError, TypeError):
            return 0

    cal = []
    data = []
    tools_total = 0
    cost_total = 0
    partner_fee_total = 0
    format_ = '%Y-%m-%d'
    months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    for i in range(1, 14):
        if i == 13:
            value = f'1406-01-01'
        else:
            value = f'1405-{i:02d}-01'
        jalali_date = jalali_datetime.strptime(force_str(value), format_).togregorian().date()
        cal.append(jalali_date)
    for i in range(len(cal) - 1):
        month_data = Customer.objects.filter(date__gte=cal[i], date__lt=cal[i + 1]).aggregate(
            tools_total=models.Sum('tools_total'),
            cost_total=models.Sum('cost_total'),
        )
        month_data2 = Customer.objects.filter(date__gte=cal[i], date__lt=cal[i + 1])
        fee = 0
        for q in month_data2:
            fee += multiply_by_million(q.partner_fee or 0)
        tools_total += month_data['tools_total'] or 0
        cost_total += month_data['cost_total'] or 0
        partner_fee_total += fee
        data.append({
            'date': months[i],
            'tools_total': f"{month_data['tools_total'] or 0:,}",
            'cost_total': f"{month_data['cost_total'] or 0:,}",
            'partner_fee': f"{(fee):,}",
        })
    data.append({
        'date': 'جمع کل',
        'tools_total': f"{tools_total:,}",
        'cost_total': f"{cost_total:,}",
        'partner_fee': f"{(partner_fee_total):,}",
    })
    print((partner_fee_total))
    return render(request, 'management/report.html', {'objects': data})