![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## Фонд помощи котикам

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Технологии:

- Python 3.9
- FastAPI
- FastAPI Users
- SQLAlchemy
- Alembic

## Запуск:

Для начала работы необходимо клонировать репозиторий:

```bash
git clone git@github.com:Kolbacyn/cat_charity_fund.git
```

Установить и активировать виртуальное окружение:

```bash
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла `requirements.txt`:

```bash
pip install -r requirements.txt
```

Создать файл `.env` с настройками:

```bash
APP_TITLE=<Ваше название приложения>
DESCRIPTION=<Ваше описание проекта>
VERSION=0.4.0
DATABASE_URL=<Настройки подключения к БД, например: sqlite+aiosqlite:///./development.db>
FIRST_SUPERUSER_EMAIL = <Ваш e-mail>
FIRST_SUPERUSER_PASSWORD = <Ваш пароль>
```

Применить миграции для создания БД:

```bash
alembic upgrade head
```

Запустить приложение:

```bash
uvicorn app.main:app
```

## Документация API будет доступна по адресу:

```bash
http://127.0.0.1:8000/docs
```

## Разработчик

[Зольников Юрий](https://github.com/Kolbacyn/)