from django.shortcuts import render
from  rest_framework import viewsets, status
from  rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Movie, rating
from .serializers import MovieSerializer, ratingSerializer, UserSerializer

# Create your views here.

#can allow users to register
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer #accepts only one
    authentication_classes = (TokenAuthentication, )
    permission_classes  = (AllowAny, ) 

    #to implement custom method
    @action(detail=True, methods=['POST']) #detail=True: one specific movie, False=al the list of movies
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user 
            
            ##o/p: AnonymousUser since django doesn't know the user as they are not LOGGED IN, so no AUTHENTICATION
            #static user declaration(fixed for example)
            #user = User.objects.get(id=2) #hardcoded
            #print('user', user.username)
            #print('movie tilte', movie.title) #pk: primary key = by default id is pk
           
            #check if rating is present for a specific user and movie, save rating
            try:
                rate = rating.objects.get(user=user.id, movie=movie.id)
                rate.stars = stars
                rate.save()
                serializer = ratingSerializer(rate, many=False)
                response = {'message' : 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            
            #if rating not present, create new object with user, movie, stars 
            except:
                rate = rating.object.create(user=user, movie=movie, stars=stars)
                serializer = ratingSerializer(rate, many=False)
                response = {'message' : 'Rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
             
        else:
            response = {'message' : 'give stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ratingViewSet(viewsets.ModelViewSet):
    queryset = rating.objects.all()
    serializer_class = ratingSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes  = (IsAuthenticated, ) #can restrict some users (a certain part of our application) from seeing: should have Authorization CHECKED ON in the Header 

    #creating methods overriding the default ones: for create and update
    def update(self, request, *args, **kwargs):
        response = {'message': 'The rating cannot be updated this way'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {'message': 'The rating cannot be created this way'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
