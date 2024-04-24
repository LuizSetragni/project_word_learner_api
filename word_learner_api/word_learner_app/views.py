from rest_framework.response import Response
from rest_framework.decorators import api_view
from nltk.corpus import wordnet
from .models import Word

@api_view(['POST'])
def save_word(request):
    if request.method == 'POST':
        data = request.data

        word_content = data.get('word')
        link = data.get('link')

        if word_content.isalpha():
            synsets = wordnet.synsets(word_content)
            meanings = []
            synonyms = []
            
            for synset in synsets[:3]:
                meanings.append(synset.definition())
                synonyms.extend([lemma.name() for lemma in synset.lemmas()][:3])

            word_obj = Word.objects.create(
                content=word_content,
                link=link,
                synonym_1=synonyms[0] if synonyms else None,
                synonym_2=synonyms[1] if len(synonyms) > 1 else None,
                synonym_3=synonyms[2] if len(synonyms) > 2 else None,
                meaning_1=meanings[0] if meanings else None,
                meaning_2=meanings[1] if len(meanings) > 1 else None,
                meaning_3=meanings[2] if len(meanings) > 2 else None,
            )

            response_data = {
                'id': word_obj.id,
                'content': word_content,
                'link': link,
                'meanings': meanings,
                'synonyms': synonyms,
            }
            return Response(response_data)
        else:
            return Response({"error": "Não é uma palavra válida: '{}'".format(word_content)})

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, world!"})

