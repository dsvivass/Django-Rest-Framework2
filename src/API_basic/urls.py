from django.urls import path, include
from rest_framework import routers
from .views import article_list, article_detail, ArticleAPIView, ArticleDetailsAPIView, GenericAPIView, ArticleViewSet, ArticleGenericViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')

router2 = DefaultRouter()
router2.register('articleGeneric', ArticleGenericViewSet, basename='genericArticle')

urlpatterns = [
    # path('article/', article_list),
    # path('detail/<int:id>/', article_detail),
    # path('article/', ArticleAPIView.as_view()),
    # path('detail/<int:id>/', ArticleDetailsAPIView.as_view()),
    path('generic/article/<int:id>', GenericAPIView.as_view()),

    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls)),

    path('viewset/', include(router2.urls)),
    path('viewset/<int:pk>/', include(router2.urls)),
]
