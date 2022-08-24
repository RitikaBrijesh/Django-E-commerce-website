# Generated by Django 4.0.5 on 2022-07-14 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_color_size'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name_plural': '2. Brands'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': '1. Categories'},
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name_plural': '3. Colors'},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'verbose_name_plural': '4. Sizes'},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=400)),
                ('detail', models.TextField()),
                ('specs', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
            options={
                'verbose_name_plural': '6. Products',
            },
        ),
    ]