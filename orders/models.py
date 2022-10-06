from django.db import models
from django.conf import settings
from course.models import Course
from django.shortcuts import reverse

# Create your models here.

choices = (
    ('0', 'Chưa thanh toán'),
    ('1', 'Đã thanh toán'),
)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(choices=choices, max_length=10, default='0')
    total_price = models.FloatField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_absolute_url(self):
        return reverse('orders:invoice', kwargs={'pk': self.pk})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='ordered')
    total = models.FloatField(null=False, blank=False)

    def __str__(self):
        return f'Order Item {self.id}'
