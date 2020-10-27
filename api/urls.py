from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import PostViewSet, CommentViewSet

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router = DefaultRouter()
router.register('v1/posts', PostViewSet)
router.register('v1/posts/' + r'(?P<id>[^/.]+)' + '/comments', CommentViewSet, 'comment')

urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('v1/api-token-auth/', views.obtain_auth_token),
]