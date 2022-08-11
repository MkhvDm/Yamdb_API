from django.core.management.base import BaseCommand
import csv
from reviews import models
from users.models import User

models_assignments = {
    'users': User,
    'category': models.Category,
    'genre': models.Genre,
    'titles': models.Title,

    'genre_title': models.TitleGenre,
    'review': models.Review,
    'comments': models.Comment,

}

# names in csv for foreign key relations.
# key - name of csv file,
# value - tuple of variants of names in csv table's columns
fk_names = {
    'category': ('category_id', 'category'),
    'users': ('author', 'users', 'author_id', 'user_id', ),
}

ALREADY_LOADED_ERROR_MESSAGE = (
    'Кажется, в базе уже есть данные. Попробуйте удалить файл db, выполнить '
    'миграции и запустить команду заново.'
)


class Command(BaseCommand):
    help = 'Load data in database (SQLite3) from CSV-file.'

    def handle(self, *args, **options):
        if models.Title.objects.exists():
            print('Data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        table_names = list(models_assignments.keys())
        for table in table_names:
            csv_file = f'static/data/{table}.csv'
            with open(csv_file, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    model = models_assignments.get(table)
                    for key in row.keys():  # foreign key fields update
                        for item in fk_names.items():
                            if key in item[1]:
                                fk_model = models_assignments[item[0]]
                                fk_inst = fk_model.objects.get(pk=int(row[key]))
                                row[key] = fk_inst
                    model.objects.update_or_create(**row)
            print(f'Loading "{table}" done!')
        print('Load complete!')
