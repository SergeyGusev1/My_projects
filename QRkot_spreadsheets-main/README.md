# QRkot_spreadsheets 🐱

Сервис для сбора пожертвований на благотворительные проекты с автоматическим закрытием сборов и экспортом отчётов в Google Sheets.

## ✨ Возможности
- 📊 Создание благотворительных проектов
- 💸 Приём пожертвований
- ✅ Автоматическое закрытие проекта при достижении цели
- 📈 Выгрузка отчётов в Google Таблицы

## 🛠 Стек технологий
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-✓-green?style=flat-square&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-✓-red?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-✓-blue?style=flat-square&logo=postgresql)
![Google Sheets API](https://img.shields.io/badge/Google%20Sheets%20API-✓-green?style=flat-square&logo=google)

## 🚀 Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/SergeyGusev1/QRkot_spreadsheets.git
cd QRkot_spreadsheets

# Создать виртуальное окружение
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Linux/Mac

# Установить зависимости
pip install -r requirements.txt

# Настройка .env (скопировать и заполнить)
cp .env.example .env

# Запустить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload
