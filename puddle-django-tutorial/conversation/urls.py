from django.urls import path

from . import views
from .views import new_conversation, inbox

app_name = 'conversation'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/<int:item_id>/', new_conversation, name='new'),
]