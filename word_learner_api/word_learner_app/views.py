from datetime import datetime, timedelta
import json
from typing import Counter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Word
from .word_processing import save_word
import re
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncDay
from django.db.models import Count

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crawl_and_save_words(request):
    data = request.data
    url = data.get('url')
    user = request.user 

    if url:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            if text and detect(text) == 'en':
                words = text.split()
                for word in words:
                    word = re.sub(r'[^a-zA-Z]', '', word)
                    if word and not Word.objects.filter(content=word).exists():
                        save_word(word, url, user)
                        print(word)
                return Response({"message": "Palavras extraídas e salvas com sucesso."}, status=200)
            else:
                return Response({"error": "O texto não está em inglês ou não foi possível detectar o idioma."}, status=400)
        else:
            return Response({"error": "Erro ao acessar a página: {}".format(response.status_code)}, status=400)
    else:
        return Response({"error": "URL não fornecida."}, status=400)

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_words_content_by_user_id(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    words = Word.objects.filter(user=user).order_by('content')
    word_list = [{'id': word.id, 'content': word.content} for word in words]
    return JsonResponse({'word_list': word_list})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_word_detail_by_id(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    
    word_detail = {
        'id': word.id,
        'content': word.content,
        'link': word.link,
        'phrase_1': word.phrase_1,
        'phrase_2': word.phrase_2,
        'phrase_3': word.phrase_3,
        'synonym_1': word.synonym_1,
        'synonym_2': word.synonym_2,
        'synonym_3': word.synonym_3,
        'meaning_1': word.meaning_1,
        'meaning_2': word.meaning_2,
        'meaning_3': word.meaning_3,
        'created_at': word.created_at,
        'user_id': word.user_id
    }
    
    return JsonResponse({'word': word_detail})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_links_by_user_id(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    words = Word.objects.filter(user=user).values_list('link', flat=True)
    link_counts = Counter(link for link in words if link)
    sorted_links = sorted(link_counts.items(), key=lambda x: x[1], reverse=True)
    
    response = [{'link': link, 'count': count} for link, count in sorted_links]
    
    return JsonResponse(response, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_word_count_by_day_last_week(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    words = (Word.objects
             .filter(user=user, created_at__range=[start_date, end_date])
             .annotate(day=TruncDay('created_at'))
             .values('day')
             .annotate(count=Count('id'))
             .order_by('day'))
    
    word_counts = {entry['day'].strftime('%A'): entry['count'] for entry in words}
    
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    response = {day: word_counts.get(day, 0) for day in days_of_week}
    
    total_words = sum(response.values())
    average_words_per_day = total_words / len(days_of_week)
    
    response['average'] = int(average_words_per_day)
    
    return JsonResponse(response)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_words_by_link_and_user_id(request):
    User = get_user_model()
    
    data = json.loads(request.body)
    user_id = data.get('user_id')
    link = data.get('link')

    if user_id is None or link is None:
        return JsonResponse({'error': 'user_id and link are required'}, status=400)

    user = get_object_or_404(User, id=user_id)

    words = Word.objects.filter(user=user, link=link).values('id', 'content')

    return JsonResponse({'words': list(words)})