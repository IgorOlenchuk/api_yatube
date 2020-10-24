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

    def retrieve(self, request, **kwargs):
        post = get_object_or_404(self.queryset, pk=kwargs['pk'])
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, **kwargs):
        post = get_object_or_404(self.queryset, pk=kwargs['pk'])
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, **kwargs):
        post = get_object_or_404(self.queryset, pk=kwargs['pk'])
        serializer = PostSerializer(post, data=request.data, partial=True)
        self.check_object_permissions(self.request, post)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, **kwargs):
        post = get_object_or_404(self.queryset, pk=kwargs['pk'])
        self.check_object_permissions(self.request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def retrieve(self, request, **kwargs):
        comment = get_object_or_404(self.queryset)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, **kwargs):
        comment = get_object_or_404(self.queryset)
        serializer = CommentSerializer(comment, data=self.request.data, partial=True)
        self.check_object_permissions(self.request, comment)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, **kwargs):
        comment = Comment.objects.get(id=self.kwargs['pk'])
        serializer = CommentSerializer(comment, data=self.request.data, partial=True)
        self.check_object_permissions(self.request, comment)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def destroy(self, request, **kwargs):
        comment = Comment.objects.get(id=self.kwargs['pk'])
        self.check_object_permissions(self.request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
