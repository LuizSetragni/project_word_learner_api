from django.urls import path
from .views import crawl_and_save_words, get_links_by_user_id, get_word_count_by_day_last_week, get_word_detail_by_id, get_words_by_link_and_user_id, get_words_content_by_user_id
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

    path('words/contents/<int:user_id>/', get_words_content_by_user_id, name='get_words_content_by_user_id'),
    path('words/links/<int:user_id>/', get_links_by_user_id, name='get_links_by_user_id'),
    path('word/detail/<int:word_id>/', get_word_detail_by_id, name='get_word_detail_by_id'),
    path('words/count/last_week/<int:user_id>/', get_word_count_by_day_last_week, name='get_word_count_by_day_last_week'),
    path('words/by_link/', get_words_by_link_and_user_id, name='get_words_by_link_and_user_id'),
]
