import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'word_learner_api.settings')

application = get_wsgi_application()

app = application