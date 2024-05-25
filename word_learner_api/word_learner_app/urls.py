from django.urls import path
from .views import crawl_and_save_words
from .views import UserRegistrationView
from .serializers import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('crawl_and_save_words/', crawl_and_save_words, name='crawl_save'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
