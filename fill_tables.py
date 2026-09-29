import os
import django

# Подключаем настройки нашего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from bookings.models import Zone, Table

# Находим наши созданные зоны
zone_center = Zone.objects.get(name__icontains="Центральный")
zone_window = Zone.objects.get(name__icontains="окон")
zone_sofa = Zone.objects.get(name__icontains="диван")

# Список всех 17 столов
tables_data = [
    # 1. Центральный зал (столы 1-6 на 4 чел)
    {"number": 1, "seats": 4, "map_id": "table_c1", "zone": zone_center},
    {"number": 2, "seats": 4, "map_id": "table_c2", "zone": zone_center},
    {"number": 3, "seats": 4, "map_id": "table_c3", "zone": zone_center},
    {"number": 4, "seats": 4, "map_id": "table_c4", "zone": zone_center},
    {"number": 5, "seats": 4, "map_id": "table_c5", "zone": zone_center},
    {"number": 6, "seats": 4, "map_id": "table_c6", "zone": zone_center},

    # 2. У окон (столы 7-12 на 2 чел)
    {"number": 7, "seats": 2, "map_id": "table_w1", "zone": zone_window},
    {"number": 8, "seats": 2, "map_id": "table_w2", "zone": zone_window},
    {"number": 9, "seats": 2, "map_id": "table_w3", "zone": zone_window},
    {"number": 10, "seats": 2, "map_id": "table_w4", "zone": zone_window},
    {"number": 11, "seats": 2, "map_id": "table_w5", "zone": zone_window},
    {"number": 12, "seats": 2, "map_id": "table_w6", "zone": zone_window},

    # 3. Мягкие диваны (столы 13-17 на 4 и 6 чел)
    {"number": 13, "seats": 4, "map_id": "table_sofa_1", "zone": zone_sofa},
    {"number": 14, "seats": 4, "map_id": "table_sofa_2", "zone": zone_sofa},
    {"number": 15, "seats": 4, "map_id": "table_sofa_3", "zone": zone_sofa},
    {"number": 16, "seats": 6, "map_id": "table_sofa_4", "zone": zone_sofa},
    {"number": 17, "seats": 6, "map_id": "table_sofa_5", "zone": zone_sofa},
]

# Записываем в базу данных
for data in tables_data:
    Table.objects.update_or_create(
        number=data["number"],
        defaults=data
    )

print("🎉 УРА! Все 17 столов успешно добавлены в базу данных!")