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
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated

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