import uuid

from django.db import models


class Game(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=250)
    release_date = models.CharField(max_length=250)
    official_website = models.CharField(max_length=250)
    developer = models.CharField(max_length=250)
    publisher = models.CharField(max_length=250)
    platforms = models.CharField(max_length=250)
    pegi = models.CharField(max_length=250)
    tags = models.CharField(max_length=250)
    image_url = models.CharField(max_length=250, default='No image')
    page_url = models.CharField(max_length=250, default='No page url')


class ListGame(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    merchant = models.CharField(max_length=250)
    price = models.CharField(max_length=250)
    href = models.CharField(max_length=250)
