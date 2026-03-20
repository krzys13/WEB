from rest_framework import serializers, generics
from .models import Category, Ingredient, Cocktail, CocktailIngredient
from django.contrib.auth.models import User
from rest_framework import validators




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]
        validators = [validators.UniqueValidator(
            queryset=Category.objects.all(),
            message="Category with this name already exists."
        )]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name can not be empty or whitespaces.")
        return value

        

class IngredientSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "author",
        ]
    def validate_name(self, value):
        if not value.strip():  
            raise serializers.ValidationError("Name can not be empty or whitespaces.")
        return value

class CocktailIngredientSerializer(serializers.ModelSerializer):
    cocktail_name = serializers.ReadOnlyField(source="cocktail.name")
    ingredient_name = serializers.ReadOnlyField(source="ingredient.name")
    author = serializers.ReadOnlyField(source="author.username")

    cocktail_id = serializers.PrimaryKeyRelatedField(
        queryset=Cocktail.objects.all(),
        source="cocktail",
        write_only=True,
        required =True,
    )
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source="ingredient",
        write_only = True,
        required = True,
    )

    class Meta:
        model = CocktailIngredient
        fields = [
            "id",
            "cocktail_name",
            "cocktail_id",
            "ingredient_name",
            "ingredient_id",
            "amount",
            "author",
        ]
        validators = [serializers.UniqueTogetherValidator(
            queryset=CocktailIngredient.objects.all(),
            fields=['cocktail', 'ingredient'],
            message="This ingredient is already added to the cocktail."
        )]

class CocktailIngredientChildSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.ReadOnlyField(source="ingredient.name")
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = CocktailIngredient
        fields = [
            "id",
            "ingredient_name",
            "amount",
            "author",
        ] 


class CocktailSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source="category.name")
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        allow_null=True,
        required=False
    )
    author = serializers.ReadOnlyField(source="author.username")
    ingredients = CocktailIngredientChildSerializer(
        source="cocktailingredient_set",
        many=True,
        read_only=True
    )

    class Meta:
        model = Cocktail
        fields = [
            "id",
            "name",
            "category",
            "category_id",
            "instructions",
            "is_alcoholic",
            "ingredients",
            "author",
        ]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name can not be empty or whitespaces.")
        return value



class UserSerializer(serializers.ModelSerializer):
    cocktails = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "cocktails",
        ]
    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError("Username can not be empty or whitespaces.")
        return value

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer