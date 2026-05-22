import uuid
from django.db import models
from django.core.validators import MinValueValidator

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_column='created', help_text="Fecha y hora de creación del registro")
    updated_at = models.DateTimeField(auto_now=True, db_column='modified', help_text="Fecha y hora de la última modificación")

    class Meta:
        abstract = True

class Restaurant(UUIDMixin, TimeStampedMixin):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=50, default="UTC", help_text="Ej: Europe/Madrid o America/La_Paz")

    class Meta:
        db_table = '"content"."restaurant"'
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.name

class TableType(UUIDMixin, TimeStampedMixin):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='table_types')
    name = models.CharField(max_length=100, help_text="Ej: Mesa Compartida, Barra")
    seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(blank=True, null=True)
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = '"content"."table_type"'
        verbose_name = "Table Type"
        verbose_name_plural = "Table Types"

    def __str__(self):
        return f"{self.name} ({self.seats} seats) - {self.restaurant.name}"

class MenuItem(UUIDMixin, TimeStampedMixin):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    date = models.DateField(help_text="Fecha en la que este menú está disponible")
    course = models.CharField(max_length=100, help_text="Ej: Starter, Main, Dessert")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    allergens = models.JSONField(default=list, blank=True, help_text="Lista de strings con alérgenos")

    class Meta:
        db_table = '"content"."menu_item"'
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return f"{self.name} - {self.course}"

class Reservation(UUIDMixin, TimeStampedMixin):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reservations')
    table_type = models.ForeignKey(TableType, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    party_size = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')

    class Meta:
        db_table = '"content"."reservation"'
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return f"Res: {self.party_size} pax @ {self.date} {self.time}"

class ReservationGuest(UUIDMixin, TimeStampedMixin):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='guests')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True, help_text="Alergias o peticiones especiales")

    class Meta:
        db_table = '"content"."reservation_guest"'
        verbose_name = "Guest"
        verbose_name_plural = "Guests"

    def __str__(self):
        return self.name
    
class Turn(UUIDMixin, TimeStampedMixin):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='turns')
    name = models.CharField(max_length=50, help_text="Ej: Almuerzo, Cena")
    start_time = models.TimeField(help_text="Hora de inicio del turno")
    end_time = models.TimeField(help_text="Hora de fin del turno")

    class Meta:
        db_table = '"content"."turn"'
        verbose_name = "Turn"
        verbose_name_plural = "Turns"

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time}) - {self.restaurant.name}"