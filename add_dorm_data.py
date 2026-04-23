import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registration_assistant.settings')
django.setup()

from myapp.models import Dormitory

# 清空现有宿舍数据
Dormitory.objects.all().delete()

# 添加测试宿舍数据
dormitories = [
    {'building': '1号楼', 'room': '101', 'total_beds': 4, 'available_beds': 4},
    {'building': '1号楼', 'room': '102', 'total_beds': 4, 'available_beds': 3},
    {'building': '1号楼', 'room': '103', 'total_beds': 4, 'available_beds': 2},
    {'building': '1号楼', 'room': '104', 'total_beds': 4, 'available_beds': 1},
    {'building': '2号楼', 'room': '201', 'total_beds': 4, 'available_beds': 4},
    {'building': '2号楼', 'room': '202', 'total_beds': 4, 'available_beds': 0},
    {'building': '2号楼', 'room': '203', 'total_beds': 4, 'available_beds': 2},
    {'building': '3号楼', 'room': '301', 'total_beds': 6, 'available_beds': 6},
    {'building': '3号楼', 'room': '302', 'total_beds': 6, 'available_beds': 4},
    {'building': '4号楼', 'room': '401', 'total_beds': 8, 'available_beds': 8},
]

for dorm_data in dormitories:
    Dormitory.objects.create(
        building=dorm_data['building'],
        room=dorm_data['room'],
        total_beds=dorm_data['total_beds'],
        available_beds=dorm_data['available_beds'],
        is_occupied=(dorm_data['available_beds'] == 0)
    )

print(f'成功添加了 {Dormitory.objects.count()} 个宿舍')
