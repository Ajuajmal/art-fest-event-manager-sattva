# Generated by Django 2.2.9 on 2020-01-23 18:27

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0014_auto_20200123_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsresult',
            name='winners',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
