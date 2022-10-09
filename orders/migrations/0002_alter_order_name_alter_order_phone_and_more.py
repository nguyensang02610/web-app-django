# Generated by Django 4.1.1 on 2022-10-08 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=15, verbose_name='Số điện thoại'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('0', 'Chưa thanh toán'), ('1', 'Đã thanh toán')], default='0', max_length=10, verbose_name='Trạng thái'),
        ),
    ]
