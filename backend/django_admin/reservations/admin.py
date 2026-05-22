from django.contrib import admin
from .models import Restaurant, TableType, MenuItem, Reservation, ReservationGuest, Turn

class TableTypeInline(admin.TabularInline):
    model = TableType
    extra = 1 
    fields = ('name', 'seats', 'price_per_seat')

class ReservationGuestInline(admin.TabularInline):
    model = ReservationGuest
    extra = 0
    fields = ('name', 'email', 'notes')

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('course', 'name', 'price')

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'timezone', 'created_at')
    search_fields = ('name',)
    list_filter = ('timezone',)
    inlines = [TableTypeInline, MenuItemInline]

@admin.register(TableType)
class TableTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'seats', 'price_per_seat')
    list_filter = ('restaurant',)
    search_fields = ('name', 'restaurant__name')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'course', 'date', 'price')
    list_filter = ('restaurant', 'course', 'date')
    search_fields = ('name', 'description')
    date_hierarchy = 'date' 

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'table_type', 'date', 'time', 'party_size', 'status')
    list_filter = ('status', 'restaurant', 'date')
    search_fields = ('restaurant__name',)
    date_hierarchy = 'date'
    inlines = [ReservationGuestInline]

@admin.register(Turn)
class TurnAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'name', 'start_time', 'end_time')
    list_filter = ('restaurant', 'name', 'start_time', 'end_time')
    search_fields = ('name')
