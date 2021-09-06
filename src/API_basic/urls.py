from django.urls import path
from .views import article_list, article_detail, ArticleAPIView, ArticleDetailsAPIView

urlpatterns = [
    # path('article/', article_list),
    # path('detail/<int:id>/', article_detail),
    path('article/', ArticleAPIView.as_view()),
    path('detail/<int:id>/', ArticleDetailsAPIView.as_view()),
]
