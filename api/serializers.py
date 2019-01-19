from rest_framework import serializers
from main_article.models import Article , Category


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')
    author = serializers.ReadOnlyField(source='author.username')
    # category = serializers.ReadOnlyField(source='category.name')
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),allow_null=True)
    class Meta:
        model = Article
        fields = ('url','author','category','title','content','pubDateTime','upDateTime')