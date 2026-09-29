from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. ПРОФИЛИ И РОЛИ (Админ, Хостес, Гость)
# ==========================================
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Администратор'),
        ('HOSTESS', 'Хостес'),
        ('GUEST', 'Гость'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='GUEST', verbose_name="Роль")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


# ==========================================
# 2. ЗОНЫ ЗАЛА (VIP-диваны, У окна, Бар...)
# ==========================================
class Zone(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название зоны")
    description = models.TextField(blank=True, verbose_name="Описание зоны")

    class Meta:
        verbose_name = "Зона зала"
        verbose_name_plural = "Зоны зала"

    def __str__(self):
        return self.name


# ==========================================
# 3. СТОЛЫ
# ==========================================
class Table(models.Model):
    number = models.IntegerField(unique=True, verbose_name="Номер стола")
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Зона зала")
    seats = models.IntegerField(verbose_name="Вместимость (чел)")
    map_id = models.CharField(max_length=50, unique=True, verbose_name="ID на карте (SVG)")
    is_active = models.BooleanField(default=True, verbose_name="Доступен для брони")

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        ordering = ['number']

    def __str__(self):
        zone_name = f" ({self.zone.name})" if self.zone else ""
        return f"Стол №{self.number} на {self.seats} чел.{zone_name}"


# ==========================================
# 4. БРОНИРОВАНИЯ
# ==========================================
class Booking(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новая заявка'),
        ('CONFIRMED', 'Подтверждена'),
        ('SEATED', 'Гости за столом'),
        ('COMPLETED', 'Завершена'),
        ('CANCELLED', 'Отменена'),
    ]

    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name="Стол")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Аккаунт гостя (если есть)")
    
    # Данные гостя (заполняются всегда)
    guest_name = models.CharField(max_length=100, verbose_name="Имя гостя")
    guest_phone = models.CharField(max_length=20, verbose_name="Телефон")
    guests_count = models.IntegerField(default=2, verbose_name="Количество гостей")
    
    date = models.DateField(verbose_name="Дата брони")
    time_start = models.TimeField(verbose_name="Время начала")
    time_end = models.TimeField(verbose_name="Время окончания")
    
    comment = models.TextField(blank=True, verbose_name="Пожелания гостя")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-date', '-time_start']

    def __str__(self):
        return f"{self.date} {self.time_start} | Стол №{self.table.number} | {self.guest_name}"


# ==========================================
# 5. МЕНЮ (Категории и Блюда)
# ==========================================
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория меню"
        verbose_name_plural = "Категории меню"

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=150, verbose_name="Название блюда")
    description = models.TextField(blank=True, verbose_name="Описание / Состав")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (руб)")
    weight_grams = models.IntegerField(null=True, blank=True, verbose_name="Вес (г)")
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True, verbose_name="Фото")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Меню (Блюда)"

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"