from django.urls import path

from .views import board_topics, new_topic

urlpatterns = [
    path('<int:pk>/', board_topics, name='board_topics'),
    path('<int:pk>/new/', new_topic, name='new_topic')
]