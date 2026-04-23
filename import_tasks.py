#!/usr/bin/env python3
"""
为所有新生批量分配标准报到任务
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registration_assistant.settings')
django.setup()

from myapp.models import Student, RegistrationTask

# 标准报到任务列表
standard_tasks = [
    '缴纳学费',
    '宿舍入住办理',
    '领取军训物资',
    '身份核验',
    '领取校园卡'
]

def import_tasks():
    """为所有新生批量分配标准报到任务"""
    print("开始为新生分配标准报到任务...")
    
    # 获取所有新生
    students = Student.objects.all()
    total_students = students.count()
    print(f"共找到 {total_students} 名新生")
    
    created_count = 0
    
    for student in students:
        print(f"\n为新生 {student.student_id} - {student.name} 分配任务:")
        
        for task_name in standard_tasks:
            # 检查任务是否已存在
            if not RegistrationTask.objects.filter(student=student, task_name=task_name).exists():
                RegistrationTask.objects.create(
                    student=student,
                    task_name=task_name,
                    status='PENDING'  # 未完成
                )
                created_count += 1
                print(f"  已分配: {task_name}")
            else:
                print(f"  跳过（已存在）: {task_name}")
    
    print(f"\n任务分配完成！共创建 {created_count} 个新任务")
    print(f"当前数据库中共有 {RegistrationTask.objects.count()} 个报到任务")

if __name__ == "__main__":
    import_tasks()