#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import execute_from_command_line
from django.core.management import call_command
from django.apps import apps
from django.conf import settings  # Adicionando a importação do módulo de configurações do Django


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'word_learner_api.settings')
    try:
        apps.populate(settings.INSTALLED_APPS)  # Carrega os aplicativos do Django
        call_command('migrate')  # Aplica as migrações antes de iniciar o servidor
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


if __name__ == '__main__':
    main()
