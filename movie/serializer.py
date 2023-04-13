from rest_framework import serializers
from .models import Movie, Director, Genre, Review
from rest_framework.exceptions import ValidationError


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id stars text'.split()

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name age'.split()


class MovieSerializer(serializers.ModelSerializer):
    # genres = GenreSerializer(many=True)
    # director_str = serializers.SerializerMethodField()
    # filter_reviews = ReviewSerializer(many=True)
    class Meta:
        model = Movie
        fields = 'id name duration description is_hit rating director_id'.split()
        # exclude = 'updated created'.split()

    def get_director_str(self, movie):
        try:
            return movie.director.name
        except:
            return ''


class MovieValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=100)
    duration = serializers.IntegerField()
    description = serializers.CharField(required=False)
    is_hit = serializers.BooleanField()
    director_id = serializers.IntegerField()
    rating = serializers.FloatField(min_value=1, max_value=10)
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError("Director not found!")
        return director_id

    def validate_genres(self, genres):
        try:
            for i in genres:
                Genre.objects.get(id=i)
        except Genre.DoesNotExist:
            raise ValidationError('Does not found!')
        return genres