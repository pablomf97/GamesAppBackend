from django.db import models


class Article(models.Model):
    """
    This is the article model used to display
    the latest gaming news.
    """

    picture = models.CharField(max_length=250)
    headline = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    content_preview = models.CharField(max_length=250)
    link = models.URLField()

    def __str__(self):
        return self.headline
