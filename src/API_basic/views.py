from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
import rest_framework
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleModelSerializer, ArticleSerializer
from django.views.decorators.csrf import csrf_exempt

# Libs used for the Short way function

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Libs used for the Class based API views

from rest_framework.views import APIView

# Libs used for the generic and mixin views

from rest_framework import generics
from rest_framework import mixins

# Libs used for authentication

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Libs used for viewsets and routers

from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# Create your views here.

# VIEWSETS AND ROUTERS

class ArticleViewSet(viewsets.ViewSet):

    def list(self, request):

        articles = Article.objects.all()
        serializers = ArticleModelSerializer(articles, many=True)

        return Response(serializers.data)

    def create(self, request):

        serializer = ArticleModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None): # Trae solo 1 objeto con esa pk

        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleModelSerializer(article)

        return Response(serializer.data)

    def update(self, request, pk=None):

        article = Article.objects.get(pk=pk)
        serializer = ArticleModelSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)





# GENERIC VIEWS AND MIXIN, even better

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, # En esta clase hago todo lo que hacía en las de abajo
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin):

    serializer_class = ArticleModelSerializer
    queryset = Article.objects.all()

    lookup_field = 'id'

    # authentication
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):

        if id:
            return self.retrieve(request)

        else:
            return self.list(request) # Este funciona colocando el id=0 en el path

    def post(self, request, id=None):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


# CLASS BASED API VIEWS, Even better than functions, reusable code, much cleaner

class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializers = ArticleModelSerializer(articles, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializer = ArticleModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailsAPIView(APIView):

    def getObject(self, id):
        try:
            return Article.objects.get(id=id)

        except Article.DoesNotExist:
            raise HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        article = self.getObject(id)
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)

    def put(self, request, id):
        article = self.getObject(id)
        serializer = ArticleModelSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        article = self.getObject(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# Short way using functions

@api_view(['GET', 'POST'])
def article_list(request):

    if request.method == 'GET':
        articles = Article.objects.all()
        serializers = ArticleModelSerializer(articles, many=True)
        return Response(serializers.data)

    elif request.method == 'POST':
        serializer = ArticleModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, id):
    try:
        article = Article.objects.get(id=id)

    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleModelSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Long way using functions

# @csrf_exempt # Esto lo uso para forzar el saltado del token y
#               # usar Postman o insomnia para enviar requests directos
# def article_list(request):

#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializers = ArticleModelSerializer(articles, many=True)
#         return JsonResponse(serializers.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ArticleModelSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)

#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt # Esto lo uso para forzar el saltado del token y
# #               # usar Postman o insomnia para enviar requests directos
# def article_detail(request, id):
#     try:
#         article = Article.objects.get(id=id)

#     except Article.DoesNotExist:

#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = ArticleModelSerializer(article)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = ArticleModelSerializer(article, data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)

#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         article.delete()
#         return HttpResponse(status=204)