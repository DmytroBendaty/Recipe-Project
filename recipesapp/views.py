from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from . import models
from .forms import RatingForm
from django.contrib import messages

# Create your views here.


def home(request):
    recipes = models.Recipe.objects.all()
    context = {
        'recipes': recipes
    }
    return render(request, "recipesapp/recipes-home.html", context)


class RecipeListView(ListView):
    model = models.Recipe
    template_name = 'recipesapp/recipes-home.html'
    context_object_name = 'recipes'


class RecipeDetailView(DetailView):
    model = models.Recipe


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = models.Recipe
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Recipe
    fields = ['title', 'description']

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Recipe
    success_url = reverse_lazy('recipes-home')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


def about(request):
    return render(request, "recipesapp/recipes-about.html", {'title': 'About us page'})


def rate_recipe(request, pk=None):
    recipe_obj = get_object_or_404(models.Recipe, pk=pk)
    rating_form = RatingForm()

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating_value = int(rating_form.cleaned_data['rating'])
            user = request.user

            if models.RecipeRating.objects.filter(user=user, recipe=recipe_obj).exists():
                messages.error(request, "Ви вже оцінили цей рецепт.")
            else:
                models.RecipeRating.objects.create(
                    user=user, recipe=recipe_obj, rating=rating_value)
                recipe_obj.update_average_rating()
                return redirect('recipes-home')

    context = {
        'recipe': recipe_obj,
        'rating_form': rating_form, }

    return render(request, 'recipesapp/recipe_rating.html', context)
