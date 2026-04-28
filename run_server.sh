#!/bin/sh

set -e

echo "--> Iniciando script de setup..."

cd /app/pomodoro

echo "--> Verificando pacotes do sistema..."
apk add --no-cache python3 py3-pip git > /dev/null 2>&1

echo "--> Instalando/Atualizando uv..."
pip install uv --break-system-packages --quiet

echo "--> Sincronizando dependências do Python..."
if [ -f "uv.lock" ]; then
    uv sync --frozen --no-cache
else
    echo "Aviso: uv.lock não encontrado. Criando um novo..."
    uv sync --no-cache
fi

echo "--> Servidor pronto. Iniciando Gunicorn na porta 8004..."
exec uv run gunicorn --workers 2 --bind 0.0.0.0:8004 main:app
