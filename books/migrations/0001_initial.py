# Generated by Django 3.2.5 on 2022-12-06 09:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ISBN', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('cover', models.ImageField(default='default_book_cover.png', upload_to='book_cover_images')),
            ],
        ),
    ]
