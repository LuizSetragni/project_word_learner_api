import os
from django.core.wsgi import get_wsgi_application

print("Iniciando a aplicação WSGI...")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'word_learner_api.settings')

application = get_wsgi_application()

print("Aplicação WSGI iniciada com sucesso.")

app = application

print("A aplicação foi atribuída à variável 'app'.")
