import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import ingredients from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                ingredients_data = json.load(file)

                ingredients_to_create = []
                for item in ingredients_data:
                    ingredients_to_create.append(
                        Ingredient(
                            name=item['name'],
                            measurement_unit=item['measurement_unit']
                        )
                    )

                Ingredient.objects.bulk_create(ingredients_to_create)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully imported {len(ingredients_to_create)} '
                        f'ingredients'
                    )
                )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
