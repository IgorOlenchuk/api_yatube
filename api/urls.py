from django.conf import settings
from django.conf.urls.static import static

from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('posts/' + r'(?P<id>[^/.]+)' + '/comments', views.CommentViewSet)


urlpatterns = router.urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

