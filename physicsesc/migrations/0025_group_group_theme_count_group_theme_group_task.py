# Generated by Django 4.0.2 on 2022-06-14 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('physicsesc', '0024_group_group_name_group_picture_href'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_theme_count',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='Group_theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_theme_name', models.CharField(default='no name', max_length=50)),
                ('task_count', models.IntegerField(default=0)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='physicsesc.group')),
            ],
        ),
        migrations.CreateModel(
            name='Group_task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_comment', models.CharField(default='no comment', max_length=50)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='physicsesc.group')),
                ('group_theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='physicsesc.group_theme')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='physicsesc.task')),
            ],
        ),
    ]
