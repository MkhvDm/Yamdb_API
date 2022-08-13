# YAMDb API



Для наполнения базы данных тестовыми данными необходимого выполнить миграции:
```
user@machine .api_yamdb/api_yamdb/
> python manage.py migrate 
```
Затем выполнить команду:
```
> python manage.py load_db
```

### Как запустить проект:
Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```