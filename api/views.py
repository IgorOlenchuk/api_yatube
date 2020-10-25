from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from posts.models import Post, Comment

from .serializers import PostSerializer, CommentSerializer

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


@permission_classes((IsAuthorOrReadOnly, IsAuthenticated,))
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, **kwargs):
        serializer = PostSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@permission_classes((IsAuthorOrReadOnly, ))
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, **kwargs):
        comment = Comment.objects.filter(post_id=self.kwargs['id'])
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer, **kwargs):
        serializer.save(author=self.request.user, post_id=self.kwargs['id'])
