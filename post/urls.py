from django.urls import path
from .views import PostListAPIView,PostCreateAPIView,PostRerieveUpdateDestroyAPIView


urlpatterns = [
    path('posts/', PostListAPIView.as_view()),
    path('post/create/', PostCreateAPIView.as_view()),
    path('post/<uuid:pk>/', PostRerieveUpdateDestroyAPIView.as_view()),
    
]
