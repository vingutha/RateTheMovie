from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def no_of_ratings(self):
        ratings = rating.objects.filter(movie=self)#filter for each movie
        return len(ratings)

    def avg_rating(self):
        sum=0
        ratings = rating.objects.filter(movie=self) #array of all ratings of that single movie
        for i in ratings:
            sum = sum + i.stars
            if len(ratings)>0:    #check division by zero as it is undefined  
                return sum / len(ratings) 
            else:
                return 0


class rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE) #remove rating when movie is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    class Meta:
        #unique:  values of user and movie only accepted if not already present (only one user can rate a single movie)
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)



