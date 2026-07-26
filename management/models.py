from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام مشتری')
    date = models.DateField(verbose_name='تاریخ')
    machine = models.CharField(max_length=100, verbose_name='برند دستگاه')
    problems = models.TextField(verbose_name='ایراد دستگاه')
    tools = models.TextField(verbose_name='هزینه قطعات')
    tools_total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True, verbose_name='جمع هزینه قطعات')
    cost = models.TextField(verbose_name='اجرت')
    cost_total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True, verbose_name='جمع هزینه اجرت')
    total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True, verbose_name='جمع کل')
    image = models.ImageField(upload_to='customer_images/', null=True, blank=True, verbose_name='عکس دستگاه')

    class Meta:
         verbose_name_plural = "مشتری"
    
    def save(self, *args, **kwargs):
        temp_tools_total = sum(float(cost)*1000000 for cost in self.tools.split() if cost.replace('.', '').isdigit())
        if temp_tools_total < 1000000000:
            self.tools_total = temp_tools_total
        temp_cost_total = sum(float(cost)*1000000 for cost in self.cost.split() if cost.replace('.', '').isdigit())
        if temp_cost_total < 1000000000:
            self.cost_total = temp_cost_total
        temp_total = self.cost_total + self.tools_total
        if temp_total < 1000000000:
            self.total = temp_total
        super().save(*args, **kwargs)