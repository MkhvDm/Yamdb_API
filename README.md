# YAMDb API
## _Сервис с рецензиями на произведения_

## Возможности
- Оставляй рецензии на произведения разных категорий и жанров - кино, книги, музыку etc.
- Ставь оценку работам
- Коментируй рецензии других пользователей


## Запуск проекта:
Клонировать репозиторий и перейти в него в командной строке:

```
either HTTPS:
git clone https://github.com/MkhvDm/api_final_yatube.git
```
```
or SSH:
git clone git@github.com:MkhvDm/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Для наполнения базы данных тестовыми данными необходимого выполнить команду:

```
python manage.py load_db
```

Запустить проект:

```
python manage.py runserver
```

### Документация:
После запуска на localhost доступна [документация].

## Примеры:

### Регистрация:
* POST: http://127.0.0.1:8000/api/v1/auth/signup/ 
```
{
    "email": "string",
    "username": "string"
}
```
RESPONSE:
```
{
    "email": "string",
    "username": "string"
}
```
На почту придёт код подтвержения.

### Получение токена по коду из письма: 
* POST: http://127.0.0.1:8000/api/v1/auth/token/ 
```
{
    "username": "string",
    "confirmation_code": "string"
}
```
RESPONSE:
```
{
    "token": "string"
}
```

Для добавления/изменения данных через API необходимо добавить в header 
к запросу параметр 'Authorization' со значением 'Bearer TOKEN'.

### Получение произведений (постранично): 
* GET: http://127.0.0.1:8000/api/v1/titles/

RESPONSE:
```
{
  "count": 123,
  "next": "http://example.org/api/v1/titles/?limit=10&offset=10",
  "previous": null,,
  "results": [
    {
        "id": 1,
        "name": "Побег из Шоушенка",
        "year": 1994,
        "rating": 10,
        "description": null,
        "genre": [
            {
                "name": "Драма",
                "slug": "drama"
            }
        ],
        "category": {
            "name": "Фильм",
            "slug": "movie"
        }
    },
    ...
  ]
}
```

### Получение рецензий на произведение по id = title_id (постранично): 
* GET: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

RESPONSE:
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "text": "Не привыкай\n«Эти стены имеют одно свойство: сначала ты их ненавидишь, потом привыкаешь, а потом не можешь без них жить»",
            "author": "capt_obvious",
            "score": 10,
            "pub_date": "2022-08-12T12:26:24.656621Z"
        },
        ...
    ]
}
```


### Авторы

[Михаил Колесов]\
[Динар Гумиров]\
[Дмитрий Михеев] - [Telegram] 

[документация]: <http://127.0.0.1:8000/redoc/>
[Telegram]: <https://t.me/MkhvDm>

[Михаил Колесов]: <https://github.com/gazkhul>
[Динар Гумиров]: <https://github.com/dgumirov2>
[Дмитрий Михеев]: <https://github.com/MkhvDm>


