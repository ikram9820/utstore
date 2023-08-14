from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
from django.utils.text import slugify
from store.models import Product,Collection
import os


class Command(BaseCommand):
    help = 'Populates the database with collections and products'

    def handle(self, *args, **options):
        print('Populating the database...')
        current_dir = os.path.dirname(__file__)
        files = ['collections.sql','products.sql']
        file_paths = [os.path.join(current_dir, file) for file in files]
        files = iter(files)
        for file_path in file_paths:
            print(f"populating {next(files)}...")
            sql = Path(file_path).read_text()
            with connection.cursor() as cursor:
                cursor.execute(sql)

        # populating database from shell, didn't apply save() of
        # models where we are trying to slugify the title to slug 
        save()

def save():
    collections = Collection.objects.all()
    for c in collections: c.save()

    products = Product.objects.all()
    for p in products: 
        p.slug = slugify(p.title)
        p.save()
    
        
