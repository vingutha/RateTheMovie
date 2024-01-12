from rest_framework import serializers
from .models import Movie, rating
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
#to register new users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password') #password has to be hashed (and later decoded to view it)
        extra_kwargs={'password': {'write_only': True , 'required': True} } #write_only ture means can never see pwd but only write and 'required' for sending

        #already included but overwriting with our version
        def create (self, validated_data):
            user = User.objects.create_user(**validated_data) #user is created
            Token.objects.create(user=user) #token for user is created
            return user

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'no_of_ratings', 'avg_rating')

class ratingSerializer(serializers.ModelSerializer):
    class Meta:
        model = rating
        fields = ('id', 'stars', 'user', 'movie')