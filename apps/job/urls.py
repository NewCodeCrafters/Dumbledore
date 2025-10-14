from django.urls import path, include
from rest_framework.routers import DefaultRouter # type: ignore
from .views import JobViewSet

router = DefaultRouter()
router.register(r'jobs', JobViewSet)

urlpatterns = [
    path('router/', include(router.urls)),
    
]
