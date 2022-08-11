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

