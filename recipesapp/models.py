from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    average_rating = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)

    def update_average_rating(self):
        ratings = RecipeRating.objects.filter(recipe=self)
        if ratings.exists():
            average = ratings.aggregate(Avg('rating'))['rating__avg']
            self.average_rating = round(average, 2)
            self.save()
        else:
            self.average_rating = 0
            self.save()

    def calculate_average_rating(self):
        self.update_average_rating()
        return self.average_rating

    def get_absolute_url(self):
        return reverse("recipes-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class RecipeRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'recipe'),)
