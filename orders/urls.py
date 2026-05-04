from django.urls import path
from rest_framework.routers import DefaultRouter
from orders import views

router = DefaultRouter()
router.register('', views.OrderViewSet)

urlpatterns = router.urls