from django.contrib import admin
from .models import UserProfile, Zone, Table, Booking, Category, MenuItem

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'zone', 'seats', 'map_id', 'is_active')
    list_filter = ('zone', 'is_active', 'seats')
    search_fields = ('number', 'map_id')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'guest_phone', 'table', 'date', 'time_start', 'status')
    list_filter = ('status', 'date', 'table__zone')
    search_fields = ('guest_name', 'guest_phone')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight_grams', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name',)