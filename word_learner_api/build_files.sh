#!/bin/bash

echo "Iniciando o processo de build..."

echo "Instalando dependências do Python..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Erro ao instalar dependências do Python."
    exit 1
fi

echo "Dependências instaladas com sucesso."

echo "Coletando arquivos estáticos..."
python3.9 manage.py collectstatic --noinput

if [ $? -ne 0 ]; then
    echo "Erro ao coletar arquivos estáticos."
    exit 1
fi

echo "Arquivos estáticos coletados com sucesso."

echo "Processo de build concluído."
