from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from posts.models import Post, Comment

from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['id'])

    def perform_create(self, serializer, **kwargs):
        post = get_object_or_404(Post.objects.all(), id=self.kwargs['id'])
        serializer.save(author=self.request.user, post_id=self.kwargs['id'])
