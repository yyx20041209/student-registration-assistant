from django.contrib import admin
from myapp.models import Student, RegistrationTask, FAQ

# 注册新生模型
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'id_card', 'major', 'college', 'phone', 'status')
    search_fields = ('student_id', 'name', 'id_card', 'college')
    list_filter = ('status', 'major', 'college')
    ordering = ('student_id',)

# 注册报到任务模型
@admin.register(RegistrationTask)
class RegistrationTaskAdmin(admin.ModelAdmin):
    list_display = ('student', 'task_name', 'status', 'completed_time')
    search_fields = ('student__name', 'student__student_id', 'task_name')
    list_filter = ('status',)
    ordering = ('student__student_id',)

# 注册常见问题模型
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    search_fields = ('title', 'content', 'answer')
    list_filter = ('category',)
    ordering = ('category', 'title')