from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام مشتری', null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='آدرس')
    date = models.DateField(verbose_name='تاریخ')
    machine = models.CharField(max_length=100, verbose_name='برند دستگاه')
    problems = models.TextField(verbose_name='ایراد دستگاه')
    tools = models.TextField(verbose_name='هزینه قطعات', null=True, blank=True)
    tools_total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True, verbose_name='جمع هزینه قطعات')
    partner_fee = models.CharField(max_length=9, null=True, blank=True, verbose_name='سهم همکار')
    cost = models.TextField(verbose_name='اجرت', null=True, blank=True)
    cost_total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True, verbose_name='جمع هزینه اجرت')
    debt = models.CharField(max_length=9, null=True, blank=True, verbose_name='بدهی مشتری')
    total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True, verbose_name='جمع کل')

    class Meta:
         verbose_name_plural = "مشتری"
    
    def multiply_by_million(self, value):
        if value and value.replace('.', '').isdigit():
            try:
                if len(value) == 3 and (value.find('.') == -1):
                    return int(float(value) * 1000)
                return int(float(value) * 1000000)
            except (ValueError, TypeError):
                return 0
        return 0

    def save(self, *args, **kwargs):
        temp_tools_total = sum(self.multiply_by_million(cost) for cost in self.tools.split())
        if temp_tools_total < 1000000000:
            self.tools_total = temp_tools_total
        temp_cost_total = sum(self.multiply_by_million(cost) for cost in self.cost.split())
        if temp_cost_total < 1000000000:
            self.cost_total = temp_cost_total
        temp_total = self.cost_total + self.tools_total + self.multiply_by_million(self.partner_fee)
        if temp_total < 1000000000:
            self.total = temp_total
        super().save(*args, **kwargs)