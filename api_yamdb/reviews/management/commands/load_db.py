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
    'titles': ('title_id', 'titles', 'title'),
    'genre': ('genre_id', 'genres', 'genre'),
    'users': ('author', 'users', 'author_id', 'user_id', ),
    'review': ('review_id', 'review', 'reviews'),
}


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        tables = list(models_assignments.keys())
        for table in tables:
            csv_file = f'static/data/{table}.csv'
            with open(csv_file, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    print(row)
                    model = models_assignments.get(table)
                    print('MODEL:', model)

                    # foreign key fields update:
                    for key in row.keys():
                        for item in fk_names.items():
                            print('item:', item)
                            print('item[1]:', item[1])
                            if key in item[1]:
                                fk_model = models_assignments[item[0]]
                                fk_inst = fk_model.objects.get(pk=int(row[key]))
                                row[key] = fk_inst
                                print('New row:', row)

                    inst = model.objects.update_or_create(**row)
        print('END')
