# Generated by Django 2.0 on 2019-04-04 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video_url', models.URLField()),
                ('cover_title', models.URLField()),
                ('price', models.FloatField()),
                ('duration', models.IntegerField()),
                ('profile', models.TextField()),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseCategroy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('avatar', models.URLField()),
                ('jobtitle', models.CharField(max_length=100)),
                ('profile', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='categroy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.CourseCategroy'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.Teacher'),
        ),
    ]
