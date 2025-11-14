import pandas as pd
from django.core.management.base import BaseCommand
from mi_app.models import Estudiante

class Command(BaseCommand):
    help = 'Importa estudiantes desde un CSV'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('Dataset_g08_02.csv')  # Asegúrate que esté en la raíz de tu proyecto

        for _, row in df.iterrows():
            estudiante, created = Estudiante.objects.get_or_create(
                student_id=row['id'],
                defaults={
                    'name': row['name'],
                    'age': row['age'],
                    'gender': row['gender'],
                    'university': row['university'],
                    'faculty': row['faculty'],
                    'year': row['year'],
                    'rent_total': row['rent_total'],
                    'expected_rent': row['expected_rent'],
                    'district': row['district'],
                    'latitude': row['latitude'],
                    'longitude': row['longitude'],
                    'has_pets': row['has_pets'],
                    'smoker': row['smoker'],
                    'max_commute_min': row['max_commute_min'],
                }
            )
            if created:
                self.stdout.write(f'Estudiante {row["name"]} importado.')
            else:
                self.stdout.write(f'Estudiante {row["name"]} ya existe.')
