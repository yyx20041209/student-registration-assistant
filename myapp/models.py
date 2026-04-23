from django.db import models
from django.utils import timezone

# 新生表
class Student(models.Model):
    # 报到状态选项
    STATUS_CHOICES = [
        ('UNREGISTERED', '未报到'),
        ('IN_PROGRESS', '进行中'),
        ('COMPLETED', '已完成'),
    ]
    
    student_id = models.CharField(max_length=20, primary_key=True, verbose_name='学号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    major = models.CharField(max_length=100, verbose_name='录取专业')
    college = models.CharField(max_length=100, default='未分配', verbose_name='学院归属')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='UNREGISTERED', 
        verbose_name='报到状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '新生'
        verbose_name_plural = '新生管理'
    
    def __str__(self):
        return f'{self.student_id} - {self.name}'

# 报到任务表
class RegistrationTask(models.Model):
    # 任务状态选项
    STATUS_CHOICES = [
        ('PENDING', '未完成'),
        ('COMPLETED', '已完成'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='tasks', verbose_name='关联新生')
    task_name = models.CharField(max_length=100, verbose_name='任务名称')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING', 
        verbose_name='状态'
    )
    completed_time = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '报到任务'
        verbose_name_plural = '报到任务管理'
    
    def __str__(self):
        return f'{self.student.name} - {self.task_name}'

# 常见问题表
class FAQ(models.Model):
    # 分类选项
    CATEGORY_CHOICES = [
        ('LIFE', '生活'),
        ('TEACHING', '教学'),
        ('REGISTRATION', '报到'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='问题标题')
    content = models.TextField(verbose_name='问题内容')
    answer = models.TextField(verbose_name='回答内容')
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        verbose_name='分类'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '常见问题'
        verbose_name_plural = '常见问题管理'
    
    def __str__(self):
        return self.title

# 宿舍表
class Dormitory(models.Model):
    building = models.CharField(max_length=50, verbose_name='宿舍楼')
    room = models.CharField(max_length=10, verbose_name='房间号')
    total_beds = models.IntegerField(default=4, verbose_name='总床位')
    available_beds = models.IntegerField(default=4, verbose_name='剩余床位')
    is_occupied = models.BooleanField(default=False, verbose_name='是否已满')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '宿舍'
        verbose_name_plural = '宿舍管理'
    
    def __str__(self):
        return f'{self.building}-{self.room}'

# 学生宿舍分配表
class StudentDormitory(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='dormitory', verbose_name='学生')
    dormitory = models.ForeignKey(Dormitory, on_delete=models.SET_NULL, null=True, related_name='students', verbose_name='宿舍')
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='分配时间')
    
    class Meta:
        verbose_name = '学生宿舍分配'
        verbose_name_plural = '学生宿舍分配管理'
    
    def __str__(self):
        return f'{self.student.name} - {self.dormitory}'
