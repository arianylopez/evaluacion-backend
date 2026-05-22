import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Crea superusuario usando .env para credenciales'

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stderr.write(self.style.ERROR('ERROR: No se encontraron las credenciales del superusuario en el entorno'))
            return
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'El superusuario "{username}" ya existe'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Exito: Superusuario "{username}" creado correctamente'))