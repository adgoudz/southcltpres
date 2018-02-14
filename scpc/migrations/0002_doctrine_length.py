# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scpc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beliefsdoctrine',
            name='content',
            field=models.TextField(max_length=300),
        ),
    ]
