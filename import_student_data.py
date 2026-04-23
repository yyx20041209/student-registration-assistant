#!/usr/bin/env python3
"""
批量导入新生数据到数据库
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registration_assistant.settings')
django.setup()

from myapp.models import Student

# 新生数据
student_data = [
    {
        'student_id': '20260201',
        'name': '陈杰',
        'id_card': '110101199801010001',  # 模拟身份证号
        'major': '国际经济与贸易',
        'college': '经管学院',
        'phone': '13800138001',  # 模拟手机号
        'status': 'UNREGISTERED'  # 未报到
    },
    {
        'student_id': '20260202',
        'name': '杨秀英',
        'id_card': '110101199801010002',
        'major': '会计学',
        'college': '经管学院',
        'phone': '13800138002',
        'status': 'COMPLETED'  # 已完成
    },
    {
        'student_id': '20260203',
        'name': '黄志强',
        'id_card': '110101199801010003',
        'major': '金融学',
        'college': '经管学院',
        'phone': '13800138003',
        'status': 'IN_PROGRESS'  # 进行中
    },
    {
        'student_id': '20260301',
        'name': '周涛',
        'id_card': '110101199801010004',
        'major': '法学',
        'college': '人文学院',
        'phone': '13800138004',
        'status': 'UNREGISTERED'
    },
    {
        'student_id': '20260302',
        'name': '吴芳',
        'id_card': '110101199801010005',
        'major': '汉语言文学',
        'college': '人文学院',
        'phone': '13800138005',
        'status': 'COMPLETED'
    },
    {
        'student_id': '20260303',
        'name': '徐磊',
        'id_card': '110101199801010006',
        'major': '英语',
        'college': '外国语学院',
        'phone': '13800138006',
        'status': 'IN_PROGRESS'
    },
    {
        'student_id': '20260401',
        'name': '孙丽',
        'id_card': '110101199801010007',
        'major': '临床医学',
        'college': '医学院',
        'phone': '13800138007',
        'status': 'UNREGISTERED'
    },
    {
        'student_id': '20260402',
        'name': '胡歌',
        'id_card': '110101199801010008',
        'major': '护理学',
        'college': '医学院',
        'phone': '13800138008',
        'status': 'UNREGISTERED'
    },
    {
        'student_id': '20260403',
        'name': '郭靖',
        'id_card': '110101199801010009',
        'major': '药学',
        'college': '医学院',
        'phone': '13800138009',
        'status': 'IN_PROGRESS'
    },
    {
        'student_id': '20260501',
        'name': '林黛玉',
        'id_card': '110101199801010010',
        'major': '视觉传达设计',
        'college': '艺术学院',
        'phone': '13800138010',
        'status': 'COMPLETED'
    }
]

def import_student_data():
    """批量导入新生数据"""
    print("开始导入新生数据...")
    
    # 导入新数据
    created_count = 0
    for item in student_data:
        # 检查是否已存在
        if not Student.objects.filter(student_id=item['student_id']).exists():
            Student.objects.create(**item)
            created_count += 1
            print(f"已导入: {item['student_id']} - {item['name']}")
        else:
            print(f"跳过（已存在）: {item['student_id']} - {item['name']}")
    
    print(f"\n导入完成！共导入 {created_count} 条新数据")
    print(f"当前数据库中共有 {Student.objects.count()} 条新生数据")

if __name__ == "__main__":
    import_student_data()