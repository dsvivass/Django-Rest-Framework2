from rest_framework import serializers
from .models import Article

# Usando ModelSerializer MÁS RÁPIDO
class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = ['id', 'title', 'author', 'email'] # Los campos que estén aquí son requeridos,
                                                    # menos el id que se autoincrementa
        fields = '__all__' # Si quiero que todos los campos sean requeridos


# Usando Serializer normal
class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    date = serializers.DateTimeField()

    def create(self, validatedData): # cuando en el shell uso instancia de la clase Article
                                    # .save() se invoca create()
        return Article.objects.create(validatedData)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('title', instance.author)
        instance.email = validated_data.get('title', instance.email)
        instance.date = validated_data.get('title', instance.date)

        instance.save()
        return instance