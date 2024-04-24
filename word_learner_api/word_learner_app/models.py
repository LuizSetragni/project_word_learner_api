from django.db import models

class Word(models.Model):
    # ID automático (primary key)
    id = models.AutoField(primary_key=True)

    # Conteúdo
    content = models.CharField(max_length=255)

    # Link (opcional, pode ser nulo)
    link = models.URLField(blank=True, null=True)

    # Frases 1, 2 e 3
    phrase_1 = models.TextField(blank=True, null=True)
    phrase_2 = models.TextField(blank=True, null=True)
    phrase_3 = models.TextField(blank=True, null=True)

    # Sinônimos 1, 2 e 3
    synonym_1 = models.CharField(max_length=100, blank=True, null=True)
    synonym_2 = models.CharField(max_length=100, blank=True, null=True)
    synonym_3 = models.CharField(max_length=100, blank=True, null=True)

    # Significados 1, 2 e 3
    meaning_1 = models.TextField(blank=True, null=True)
    meaning_2 = models.TextField(blank=True, null=True)
    meaning_3 = models.TextField(blank=True, null=True)

    # ID do usuário associado (chave estrangeira)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Variáveis com nomes em inglês para facilitar a referência
    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"

    def __str__(self):
        return self.content
