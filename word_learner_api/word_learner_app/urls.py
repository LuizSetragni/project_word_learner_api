from django.urls import path
from .views import ( associate_text_with_word, crawl_and_save_words, 
                    get_links_by_user_id, get_word_count_by_day_last_week, 
                    get_word_detail_by_id, get_words_by_link_and_user_id, 
                    get_words_content_by_user_id, total_words_count,
                      total_words_per_user, update_word_annotation, UserRegistrationView)
from .serializers import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('crawl_and_save_words/', crawl_and_save_words, name='crawl_save'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('total-words-per-user/', total_words_per_user, name='total_words_per_user'),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('words/contents/<int:user_id>/', get_words_content_by_user_id, name='get_words_content_by_user_id'),
    path('words/links/<int:user_id>/', get_links_by_user_id, name='get_links_by_user_id'),
    path('word/detail/<int:word_id>/', get_word_detail_by_id, name='get_word_detail_by_id'),
    path('words/count/last_week/<int:user_id>/', get_word_count_by_day_last_week, name='get_word_count_by_day_last_week'),
    path('words/by_link/', get_words_by_link_and_user_id, name='get_words_by_link_and_user_id'),
    path('word/<int:word_id>/update_annotation/', update_word_annotation, name='update_word_annotation'),
    path('total-words-count/<int:month>/<int:user_id>/', total_words_count, name='total_words_count'),
    path('associate-text-with-word/<int:word_id>/', associate_text_with_word, name='associate_text_with_word'),
]
