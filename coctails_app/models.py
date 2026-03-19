from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    author = models.ForeignKey("auth.User", related_name="categories", on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    description = models.TextField(blank=False, null=False, help_text="Description for example: 2x 50ml)")
    image = models.URLField(blank=True, null=True, help_text="URL to the image of ingredient")
    author = models.ForeignKey("auth.User", related_name="ingredients", on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Ingredients"

    def __str__(self):
        return self.name


class Cocktail(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False, help_text="Name of the cocktail")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    instructions = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='CocktailIngredient'
    )
    is_alcoholic = models.BooleanField(default=True)

    author= models.ForeignKey("auth.User", related_name="cocktails", on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Cocktails"
    def __str__(self):
        return self.name


class CocktailIngredient(models.Model):
    cocktail = models.ForeignKey(
        Cocktail,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.CharField(max_length=100, help_text='np. 50 ml, 2 plasterki, 1/2 szklanki')
    author= models.ForeignKey("auth.User", related_name="cocktail_ingredients", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.ingredient.name} dla {self.cocktail.name}: {self.amount}"
