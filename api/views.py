from rest_framework import generics,permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from main_article.models import Article
from .serializers import ArticleSerializer
from .permissions import IsSnippetOwnerOrReadOnly

@api_view(['GET'])
def api_root(request,format=None):
    return Response(
        {
        'articles':reverse('article-list',request=request,format=format)
        }
    )


class ArticleList(generics.ListCreateAPIView):
    '''
    List Create method
    '''
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
    
class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve,Update,Destroy
    '''
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsSnippetOwnerOrReadOnly)

