import logging
from .models import Word
from nltk.corpus import wordnet

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def save_word(word_content, link=None):
    if word_content.isalpha():
        synsets = wordnet.synsets(word_content)
        meanings = []
        synonyms = []
        examples = []

        for synset in synsets[:3]:
            meanings.append(synset.definition())
            synonyms.extend([lemma.name() for lemma in synset.lemmas()][:3])
            examples.extend(synset.examples()[:3])

        try:
            word_obj = Word.objects.create(
                content=word_content,
                link=link,
                synonym_1=synonyms[0] if synonyms else None,
                synonym_2=synonyms[1] if len(synonyms) > 1 else None,
                synonym_3=synonyms[2] if len(synonyms) > 2 else None,
                meaning_1=meanings[0] if meanings else None,
                meaning_2=meanings[1] if len(meanings) > 1 else None,
                meaning_3=meanings[2] if len(meanings) > 2 else None,
                phrase_1=examples[0] if examples else None,
                phrase_2=examples[1] if len(examples) > 1 else None,
                phrase_3=examples[2] if len(examples) > 2 else None,
            )
            word_obj.save()

            response_data = {
                'id': word_obj.id,
                'content': word_content,
                'link': link,
                'meanings': meanings,
                'synonyms': synonyms,
                'examples': examples,
            }
            logger.info("Palavra salva com sucesso: %s", word_content)
            return response_data
        except Exception as e:
            logger.error("Erro ao salvar a palavra: %s", e)
            return {"error": "Erro ao salvar a palavra no banco de dados."}
    else:
        logger.error("Palavra inválida: %s", word_content)
        return {"error": "Não é uma palavra válida: '{}'".format(word_content)}
