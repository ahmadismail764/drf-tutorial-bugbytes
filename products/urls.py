from django.urls import path
from products import views

urlpatterns = [
    path('', views.ProductListCreateAPIView.as_view()),
    path('info/', views.ProductInfoAPIView.as_view()),
    path('<int:product_id>/', views.ProductDetailAPIView.as_view()),
]