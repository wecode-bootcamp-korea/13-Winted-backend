# Generated by Django 3.1.3 on 2020-11-08 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0002_auto_20201105_0958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommender',
            name='contents',
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.CharField(max_length=500)),
                ('recommender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommend.recommender')),
            ],
        ),
    ]