# 🍅 Flask Pomodoro Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Framework-000000?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![uv](https://img.shields.io/badge/uv-Fastest_Manager-purple)
![License](https://img.shields.io/badge/License-MIT-green)

Aplicação web focada em produtividade utilizando a **Técnica Pomodoro**. O sistema permite que usuários se cadastrem, cronometrem seus ciclos de foco/pausa e visualizem relatórios.

O projeto foi construído seguindo o padrão **Application Factory** e utiliza o **uv** para gerenciamento determinístico de dependências e builds ultra-rápidos.

## 📋 Funcionalidades

- **Timer Pomodoro:** Ciclos de Trabalho, Pausa Curta e Pausa Longa.
- **Rastreamento de Sessões:** Registro automático de cada ciclo concluído no banco de dados.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.10, Flask.
- **Gerenciamento de Pacotes:** [uv](https://github.com/astral-sh/uv) (Gerenciamento baseado em `pyproject.toml` e `uv.lock`).
- **Infraestrutura:** Docker e Docker Compose.

## 🚀 Como Rodar

### Opção 1: Docker (Recomendado)

Esta opção garante que o ambiente seja idêntico ao de produção, isolando todas as dependências.

```bash
# 1. Construir e subir o container (usando uv para install rápido)
docker compose up --build -d

# 2. Acessar a aplicação
# Abra http://localhost:8004