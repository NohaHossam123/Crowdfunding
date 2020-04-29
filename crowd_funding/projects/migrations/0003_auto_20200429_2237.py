# Generated by Django 2.1 on 2020-04-29 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20200428_2248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tagprojects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
        migrations.RemoveField(
            model_name='tag',
            name='projects',
        ),
        migrations.AlterField(
            model_name='rate',
            name='body',
            field=models.IntegerField(verbose_name=(0, 1, 2, 3, 4)),
        ),
        migrations.AddField(
            model_name='tagprojects',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Tag'),
        ),
    ]
