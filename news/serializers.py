from rest_framework import serializers

from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    """
        This is the serializer for the model Article.
    """

    class Meta:
        model = Article
        fields = ['picture', 'headline', 'category',
                  'content_preview', 'link']
