import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from reservations.models import Restaurant, TableType, MenuItem, Reservation, ReservationGuest

class Command(BaseCommand):
    help = 'Puebla la base de datos con 300 restaurantes y 500 hijos por restaurante usando bulk_create.'

    def handle(self, *args, **options):
        fake = Faker('es_ES')
        
        RESTAURANT_PREFIXES = ["El Gran", "La Auténtica", "Bistro", "Pizzería", "Asador", "Taberna"]
        RESTAURANT_SUFFIXES = ["del Sol", "Mesa Larga", "Gourmet", "Rústico", "Imperial", "Central"]
        COURSES = ["Starter", "Main", "Dessert", "Beverage"]
        TABLE_TYPES = ["Barra", "Mesa Compartida", "Terraza", "Salón Principal", "VIP", "Jardín"]
        STATUSES = ['CONFIRMED', 'CANCELLED', 'COMPLETED']

        if Restaurant.objects.exists():
            self.stdout.write(self.style.WARNING('La base de datos ya contiene datos. Omitiendo seeding para evitar duplicidad masiva.'))
            return

        self.stdout.write(self.style.NOTICE('Iniciando el proceso de Seeding de 150,000 registros... Por favor espera.'))

        restaurants = []
        for _ in range(300):
            name = f"{random.choice(RESTAURANT_PREFIXES)} {fake.first_name()} {random.choice(RESTAURANT_SUFFIXES)}"
            restaurants.append(Restaurant(
                name=name,
                address=fake.address(),
                timezone=random.choice(["UTC", "America/La_Paz", "America/New_York", "Europe/Madrid"])
            ))
        
        Restaurant.objects.bulk_create(restaurants, batch_size=1000)
        self.stdout.write(self.style.SUCCESS('✅ 300 Restaurantes creados.'))

        inserted_restaurants = list(Restaurant.objects.all())

        table_types_to_create = []
        menu_items_to_create = []
        reservations_to_create = []
        
        now = timezone.now()

        for restaurant in inserted_restaurants:
            for _ in range(10):
                table_types_to_create.append(TableType(
                    restaurant=restaurant,
                    name=random.choice(TABLE_TYPES),
                    seats=random.randint(1, 8),
                    description=fake.sentence(),
                    price_per_seat=round(random.uniform(0, 50.0), 2)
                ))
            
            for _ in range(40):
                menu_items_to_create.append(MenuItem(
                    restaurant=restaurant,
                    date=fake.date_between(start_date='-10d', end_date='+30d'),
                    course=random.choice(COURSES),
                    name=fake.catch_phrase().title(), 
                    description=fake.text(max_nb_chars=100),
                    price=round(random.uniform(5.0, 100.0), 2),
                    allergens=[fake.word(), fake.word()] if random.choice([True, False]) else []
                ))

            for _ in range(450):
                reservations_to_create.append(Reservation(
                    restaurant=restaurant,
                    date=fake.date_between(start_date='-5d', end_date='+15d'),
                    time=fake.time_object(),
                    party_size=random.randint(1, 6),
                    status=random.choice(STATUSES)
                ))

        self.stdout.write(self.style.NOTICE('Insertando Tipos de Mesa y Menús...'))
        TableType.objects.bulk_create(table_types_to_create, batch_size=5000)
        MenuItem.objects.bulk_create(menu_items_to_create, batch_size=5000)
        
        self.stdout.write(self.style.NOTICE('Asociando y guardando Reservaciones... (Esto tomará unos segundos)'))
        
        all_tables = TableType.objects.all().values('id', 'restaurant_id')
        tables_by_restaurant = {}
        for t in all_tables:
            tables_by_restaurant.setdefault(t['restaurant_id'], []).append(t['id'])

        for res in reservations_to_create:
            res.table_type_id = random.choice(tables_by_restaurant[res.restaurant_id])

        Reservation.objects.bulk_create(reservations_to_create, batch_size=10000)
        self.stdout.write(self.style.SUCCESS(f'✅ Datos temáticos inyectados exitosamente. Total registros procesados: {Restaurant.objects.count() + TableType.objects.count() + MenuItem.objects.count() + Reservation.objects.count()}'))