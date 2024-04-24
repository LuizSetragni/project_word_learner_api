from django.db import models

class Word(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    phrase_1 = models.TextField(blank=True, null=True)
    phrase_2 = models.TextField(blank=True, null=True)
    phrase_3 = models.TextField(blank=True, null=True)
    synonym_1 = models.CharField(max_length=100, blank=True, null=True)
    synonym_2 = models.CharField(max_length=100, blank=True, null=True)
    synonym_3 = models.CharField(max_length=100, blank=True, null=True)
    meaning_1 = models.TextField(blank=True, null=True)
    meaning_2 = models.TextField(blank=True, null=True)
    meaning_3 = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"

    def __str__(self):
        return self.content
