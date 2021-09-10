from re import U
from django.contrib.auth.signals import user_logged_in
from rest_framework import serializers
from .models import Article, User
from django.contrib.auth import login, password_validation, authenticate, logout
from rest_framework.authtoken.models import Token

# User serializer

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class GetGeneralUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'is_active']


class GetUserSerializer(serializers.Serializer):
    # class Meta:
    #     model = User
    #     fields = ['email', 'password']

    email = serializers.EmailField(max_length=100)
    password = serializers.CharField()

    def validate(self, data):

        print(data)
        print(self.context)

        user = authenticate(username = data['email'], password = data['password'])

        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')

        self.context['user'] = user
        print(self.context)
        return data

    def create(self, validated_data):
        
        token, created = Token.objects.get_or_create(user = self.context['user'])
        return self.context['user'], token.key
        


        




# Usando ModelSerializer MÁS RÁPIDO
class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'email'] # Los campos que estén aquí son requeridos,
                                                    # menos el id que se autoincrementa, y la date que se toma sola
        # fields = '__all__' # Si quiero que todos los campos sean requeridos


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