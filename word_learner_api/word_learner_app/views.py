from nltk.corpus import wordnet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Word
from .word_processing import save_word
import re
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from django.http import JsonResponse

@api_view(['POST'])
def crawl_and_save_words(request):
    data = request.data
    url = data.get('url')
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            if text and detect(text) == 'en':  
                words = text.split()
                for word in words:
                    word = re.sub(r'[^a-zA-Z]', '', word)
                    if word:  
                        if not Word.objects.filter(content=word).exists(): 
                            save_word(word, url)
                return JsonResponse({"message": "Palavras extraídas e salvas com sucesso."}, status=200)
            else:
                return JsonResponse({"error": "O texto não está em inglês ou não foi possível detectar o idioma."}, status=400)
        else:
            return JsonResponse({"error": "Erro ao acessar a página: {}".format(response.status_code)}, status=400)
    else:
        return JsonResponse({"error": "URL não fornecida."}, status=400)
