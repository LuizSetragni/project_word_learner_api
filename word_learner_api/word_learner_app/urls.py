from django.urls import path
from .views import crawl_and_save_words

urlpatterns = [
    path('crawl_and_save_words/', crawl_and_save_words, name='crawl_save'),
]
