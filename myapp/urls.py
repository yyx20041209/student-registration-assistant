from django.urls import path
from myapp import views

urlpatterns = [
    # 新生注册
    path('student/register/', views.register, name='register'),
    
    # 更新学生信息
    path('student/update/', views.update_student_info, name='update_student_info'),
    
    # 到校登记
    path('student/arrival/', views.arrival_register, name='arrival_register'),
    
    # 宿舍选择
    path('student/dorm-select/', views.dorm_select, name='dorm_select'),
    
    # 获取学生任务列表
    path('student/tasks/', views.get_student_tasks, name='get_student_tasks'),
    
    # 获取学生基本信息
    path('student/info/', views.get_student_info, name='get_student_info'),
    
    # 获取常见问题列表
    path('faqs/', views.get_faqs, name='get_faqs'),
    
    # 更新任务状态
    path('task/update/', views.update_task_status, name='update_task_status'),
    
    # 智能问答接口
    path('chat/', views.chat, name='chat'),
    
    # 管理端仪表盘接口
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # 强制通过学生报到
    path('admin/force-complete/', views.force_complete, name='force_complete'),
    
    # 获取学生详情
    path('admin/student-detail/', views.get_student_detail, name='get_student_detail'),
    
    # 管理员编辑学生信息
    path('admin/edit-student/', views.admin_edit_student, name='admin_edit_student'),
    
    # 宿舍管理
    path('admin/dorms/', views.get_dorms, name='get_dorms'),
    path('admin/dorm-detail/', views.get_dorm_detail, name='get_dorm_detail'),
    path('admin/save-dorm/', views.save_dorm, name='save_dorm'),
]