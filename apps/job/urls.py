from django.urls import path, include
from rest_framework.routers import DefaultRouter # type: ignore
from .views import JobViewSet, welcome_page

router = DefaultRouter()
router.register(r'jobs', JobViewSet)

urlpatterns = [
    path('router/', include(router.urls)),
    path('', welcome_page, name='welcome_page'),
]
