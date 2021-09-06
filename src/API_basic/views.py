from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import rest_framework
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleModelSerializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def article_list(request):

    if request.method == 'GET':
        articles = Article.objects.all()
        serializers = ArticleModelSerializer(articles, many=True)
        return JsonResponse(serializers.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleModelSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def article_detail(request, id):
    try:
        article = Article.objects.get(id=id)

    except Article.DoesNotExist:

        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleModelSerializer(article)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleModelSerializer(article, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)