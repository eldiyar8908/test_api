from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from .models import Movie, Director, Genre
from .serializer import MovieSerializer, MovieValidateSerializer, DirectorSerializer, GenreSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

class DirectorListAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'


class GenreAPIViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination


@api_view(['GET'])
def test_api_view(request):
    dict_ = {
        'text': "Hello World",
        'int': 1234,
        'float': 3.565,
        'bool': True,
        'list': [1, 5, 6],
        'dict': {'key': 'value'}
    }
    return Response(data=dict_)


@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        name = serializer.validated_data.get('name')
        duration = serializer.validated_data.get('duration')
        description = serializer.validated_data.get('description')
        is_hit = serializer.validated_data.get('is_hit')
        rating = serializer.validated_data.get('rating')
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')
        movie = Movie.objects.create(name=name, duration=duration, description=description,
                                     is_hit=is_hit, rating=rating, director_id=director_id)
        movie.genres.set(genres)
        movie.save()
        return Response(data=MovieSerializer(movie).data)
    # movie_list = []
    # for movie in movies:
    #     movie_list.append({
    #         'id': movie.id,
    #         'name': movie.name,
    #         'description': movie.description,
    #         'duration': movie.duration,
    #         'rating': movie.rating,
    #         'is_hit': movie.is_hit
    #     })
    # return JsonResponse(data=movie_list, safe=False)



@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie.name = request.data.get('name')
        movie.duration = request.data.get('duration')
        movie.description = request.data.get('description')
        movie.is_hit = request.data.get('is_hit')
        movie.rating = request.data.get('rating')
        movie.director_id = request.data.get('director_id')
        genres = request.data.get('genres')
        movie.genres.set(genres)
        movie.save()
        return Response(data=MovieSerializer(movie).data)





# @api_view(['GET', 'POST'])
# def product_list_api_view(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(data=serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(data={'errors': serializer.errors},
#                             status=status.HTTP_406_NOT_ACCEPTABLE)
#         title = serializer.validated_data.get('title')
#         description = serializer.validated_data.get('description')
#         price = serializer.validated_data.get('price')
#         category_id = serializer.validated_data.get('category_id')
#         product = Product.objects.create(title=title, description=description,
#                                          price=price, category_id=category_id)
#         return Response(data=ProductSerializer(product).data)


#
# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail_api_view(request, id):
#     try:
#         product = Product.objects.get(id=id)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(data=serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = ProductValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(data={'errors': serializer.errors},
#                             status=status.HTTP_406_NOT_ACCEPTABLE)
#         product.title = serializer.validated_data.get('title')
#         product.description = serializer.validated_data.get('description')
#         product.price = serializer.validated_data.get('price')
#         product.category = serializer.validated_data.get('category')
#         product.save()
#         return Response(data=ProductSerializer(product).data)
#
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)