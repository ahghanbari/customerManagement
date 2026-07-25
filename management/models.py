from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام مشتری')
    date = models.DateField(verbose_name='تاریخ')
    machine = models.CharField(max_length=100, verbose_name='برند دستگاه')
    problems = models.TextField(verbose_name='ایراد دستگاه')
    tools = models.TextField(verbose_name='هزینه ابزار')
    tools_total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True, verbose_name='جمع هزینه ابزار')
    cost = models.TextField(verbose_name='اجرت')
    cost_total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True, verbose_name='جمع هزینه اجرت')
    image = models.ImageField(upload_to='customer_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # t = 0
        # for i in self.cost.split():
        #     if i.isdigit():
        #         t += int(i)
        # self.cost_total = t
        self.tools_total = sum(int(cost)*1000000 for cost in self.tools.split() if cost.isdigit())
        self.cost_total = sum(int(cost)*1000000 for cost in self.cost.split() if cost.isdigit())
        super().save(*args, **kwargs)