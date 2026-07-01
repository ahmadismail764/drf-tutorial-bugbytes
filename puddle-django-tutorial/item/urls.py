from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('', views.items, name='items'),
    path('new/', views.new, name='new'),
    path('<int:item_id>/', views.detail, name='detail'),
    path('<int:item_id>/delete/', views.delete, name='delete'),
    path('<int:item_id>/edit/', views.edit, name='edit'),
]