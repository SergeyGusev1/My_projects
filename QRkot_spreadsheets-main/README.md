# QRkot_spreadseets
QRKot - сервис для сбора пожертвований на благотворительные проекты.
Возможности:
Создать благотворительный проект.
Принимать пожертвования и автомитическое закрытия проектов когда сумма закрыта.
Сделать отчёт в google sheet api.

Используемые технологии: Python 3.10, FastAPI, SQLAlchemy, Alembic, PostgreSQL/SQLite, Pytest, Aiogoogle, Google Sheet API v4, Google Drive API v3

Руководство по локальному запуску:

Клонирование репозитория: git clone https://github.com/SergeyGusev1/cat_charity_fund.git cd cat_charity_fund

Создать и активировать виртуальное окружение: python -m venv venv source venv/Scripts/activate

Установить зависимости: pip install -r requirements.txt

Создать файл .env: cp .env.example .env

Заполнить файл .env. Пример: 
APP_TITLE=Сервис пожертвований
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret
TYPE=service_account
PROJECT_ID=sergey-project-479611
PRIVATE_KEY_ID=8587c71d3f10a487c34fdccc4c0d0a91b48eec63
PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n
CLIENT_EMAIL=lazyx3@sergey-project-479611.iam.gserviceaccount.com
CLIENT_ID=114026429794968346006
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/lazyx3%40sergey-project-479611.iam.gserviceaccount.com
EMAIL=pypracticumstudents@gmail.com

Запустить миграции: alembic upgrade head

Запустить проект: uvicorn app.main:app --reload

OpenAPI по адресу: http://127.0.0.1:8000/docs