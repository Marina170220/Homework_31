# Generated by Django 4.0.4 on 2022-06-04 13:34

import Homework_27.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_date_joined_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(null=True, validators=[Homework_27.validators.check_age]),
        ),
    ]