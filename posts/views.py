from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from posts.models import Post
from posts.serializer import PostSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()

        title = request.query_params.get('title', None)
        if title is not None:
            posts = posts.filter(title_icontains=title)

        posts_serializer = PostSerializer(posts, many=True)
        return JsonResponse(posts_serializer.data, safe=False)

    elif request.method == 'POST':
        post_data = JSONParser().parse(request)
        post_serializer = PostSerializer(data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse(post_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        post_serializer = PostSerializer(post)
        return JsonResponse(post_serializer.data)

    elif request.method == 'PUT':
        post_data = JSONParser().parse(request)
        post_serializer = PostSerializer(post, data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse(post_serializer.data)
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def post_list_puplished(request):
    posts = Post.objects.filter(published=True)

    if request.method == 'GET':
        post_serializer = PostSerializer(posts, many=True)
        return JsonResponse(post_serializer.data, safe=False)
