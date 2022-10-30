# Сервис сбора пожертвований на нужды котиков QRKot

### Разработчик:

 - [Мирошниченко Евгений Игоревич](https://github.com/Eugenii1996)

### О проекте:

Проект представляет собой сервис по сбору средств на различные целевые проекты: 
на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, 
на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
Андминистратор добавляет новые проекты пожертвований, а зарегистрированные пользователи могут просто 
вносить свои средства, которые будут автоматически распределены в наиболее ранние проекты.
У адмимистратора есть возможность получать отчеты о завершенных проектах в Google Sheets.

Примененные технологии:
 - Python 3
 - Fast API
 - Git
 - Pytest
 - SQLAlchemy
 - Alembic
 - Uvicorn
 - Google Sheets API
 - Google Drive API

### Клонирование репозитория и переход в него в командной строке:

```bash
git clone git@github.com:Eugenii1996/cat_charity_fund.git
```

```bash
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```bash
pyhton -m venv venv
```

* Если у вас Linux/MacOS

    ```bash
    source venv/bin/activate
    ```

* Если у вас windows

    ```bash
    source venv/scripts/activate
    ```

### Установка зависимостей из файла requirements.txt:

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

### Запуск проекта:

Из корневой деректории проекта cat_charity_fund выполнить команды:

* Для инициализации Alembic в проекте:

    ```bash
    alembic init --template async alembic
    ```

* Для автоматического создания миграций:

    ```bash
    alembic revision --autogenerate -m "Example migration name"
    ```

* Для применения последней миграции:

    ```bash
    alembic upgrade head
    ```

* Для отмены последней миграций:

    ```bash
    alembic downgrade -1
    ```

* Для запуска сервера:

    ```bash
    uvicorn app.main:app --reload 
    ```
