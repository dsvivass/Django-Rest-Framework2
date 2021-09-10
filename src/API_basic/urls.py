from django.urls import path, include
from rest_framework import routers
from .views import article_list, article_detail, ArticleAPIView, ArticleDetailsAPIView, GenericAPIView, ArticleViewSet, ArticleGenericViewSet, UserModalViewSet, Login, UserViewSet2, logout

from rest_framework.routers import DefaultRouter

# Lib para la creacion del token
from rest_framework.authtoken import views

# router = DefaultRouter()
# router.register('article', ArticleViewSet, basename='article')

router2 = DefaultRouter()
router2.register('articleGeneric', ArticleGenericViewSet, basename='genericArticle')

router3 = DefaultRouter()
router3.register('users', UserModalViewSet, basename='users')

router4 = DefaultRouter()
router4.register('login', UserViewSet2, basename='login')

urlpatterns = [
    # path('article/', article_list),
    # path('detail/<int:id>/', article_detail),
    # path('article/', ArticleAPIView.as_view()),
    # path('detail/<int:id>/', ArticleDetailsAPIView.as_view()),
    path('generic/article/<int:id>', GenericAPIView.as_view()),

    # path('viewset/', include(router.urls)),
    # path('viewset/<int:pk>/', include(router.urls)),

    path('viewset/', include(router2.urls)),
    path('viewset/<int:pk>/', include(router2.urls)),

    # path('signup/', UserModalViewSet.as_view()),

    path('signup/', include(router3.urls)),

    path('login/', Login.as_view()),

    path('logout/', logout.as_view()),

    path('apilogin/', include(router4.urls)),
    # path('login/<str:email>/', include(router4.urls)),

    path('apiGenerateToken/', views.obtain_auth_token), # Cuando accedo a esta vista con POST me ayuda a obtener el token
]
