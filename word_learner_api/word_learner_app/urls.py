from django.urls import path
from .views import save_word

urlpatterns = [
    path('save-word/', save_word, name='save_word'),
]
