from django.urls import path
from .views import article_list, article_detail, ArticleAPIView, ArticleDetailsAPIView, GenericAPIView

urlpatterns = [
    # path('article/', article_list),
    # path('detail/<int:id>/', article_detail),
    # path('article/', ArticleAPIView.as_view()),
    # path('detail/<int:id>/', ArticleDetailsAPIView.as_view()),
    path('generic/article/<int:id>', GenericAPIView.as_view()),
]
