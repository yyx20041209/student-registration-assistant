from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Student, RegistrationTask, FAQ, Dormitory, StudentDormitory
import json
from django.db.models import Q

@require_http_methods(["GET"])
def get_student_tasks(request):
    """获取指定学生的任务列表"""
    student_id = request.GET.get('student_id')
    
    if not student_id:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': '请提供学号'
            }, ensure_ascii=False),
            content_type='application/json',
            status=400
        )
    
    try:
        # 获取学生信息
        student = Student.objects.get(student_id=student_id)
        
        # 获取该学生的所有任务
        tasks = RegistrationTask.objects.filter(student=student)
        
        # 构建任务列表数据
        task_list = []
        for task in tasks:
            task_data = {
                'id': task.id,
                'task_name': task.task_name,
                'status': task.status,
                'status_display': task.get_status_display(),
                'completed_time': task.completed_time.strftime('%Y-%m-%d %H:%M:%S') if task.completed_time else None
            }
            task_list.append(task_data)
        
        # 构建学生信息
        student_data = {
            'student_id': student.student_id,
            'name': student.name,
            'major': student.major,
            'college': student.college,
            'phone': student.phone,
            'status': student.status,
            'status_display': student.get_status_display()
        }
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'data': {
                    'student': student_data,
                    'tasks': task_list
                }
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Student.DoesNotExist:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': '未找到该学生'
            }, ensure_ascii=False),
            content_type='application/json',
            status=404
        )
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@require_http_methods(["GET"])
def get_student_info(request):
    """获取学生基本信息"""
    student_id = request.GET.get('student_id')
    
    if not student_id:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': '请提供学号'
            }, ensure_ascii=False),
            content_type='application/json',
            status=400
        )
    
    try:
        student = Student.objects.get(student_id=student_id)
        
        student_data = {
            'student_id': student.student_id,
            'name': student.name,
            'major': student.major,
            'college': student.college,
            'phone': student.phone,
            'status': student.status,
            'status_display': student.get_status_display()
        }
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'data': student_data
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Student.DoesNotExist:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': '未找到该学生'
            }, ensure_ascii=False),
            content_type='application/json',
            status=404
        )
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@require_http_methods(["GET"])
def get_faqs(request):
    """获取常见问题列表"""
    try:
        category = request.GET.get('category')
        
        if category:
            # 按分类筛选
            faqs = FAQ.objects.filter(category=category)
        else:
            # 获取所有问题
            faqs = FAQ.objects.all()
        
        faq_list = []
        for faq in faqs:
            faq_data = {
                'id': faq.id,
                'title': faq.title,
                'content': faq.content,
                'answer': faq.answer,
                'category': faq.category,
                'category_display': faq.get_category_display()
            }
            faq_list.append(faq_data)
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'data': faq_list
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def update_task_status(request):
    """更新任务状态"""
    task_id = request.POST.get('task_id')
    status = request.POST.get('status')
    
    if not task_id or not status:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': '请提供任务ID和状态'
            }, ensure_ascii=False),
            content_type='application/json',
            status=400
        )
    
    try:
        task = RegistrationTask.objects.get(id=task_id)
        
        # 更新任务状态
        task.status = status
        
        # 如果状态为已完成，记录完成时间
        if status == 'COMPLETED':
            from django.utils import timezone
            task.completed_time = timezone.now()
        
        task.save()
        
        # 自动更新学生总状态
        student = task.student
        all_tasks = RegistrationTask.objects.filter(student=student)
        completed_tasks = all_tasks.filter(status='COMPLETED')
        
        if completed_tasks.count() == all_tasks.count() and all_tasks.count() > 0:
            # 所有任务都已完成，更新为已报到
            student.status = 'COMPLETED'
        elif completed_tasks.count() > 0:
            # 部分任务已完成，更新为进行中
            student.status = 'IN_PROGRESS'
        else:
            # 没有任务完成，保持未报到状态
            student.status = 'UNREGISTERED'
        
        student.save()
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'message': '任务状态更新成功',
                'data': {
                    'id': task.id,
                    'task_name': task.task_name,
                    'status': task.status,
                    'status_display': task.get_status_display(),
                    'completed_time': task.completed_time.strftime('%Y-%m-%d %H:%M:%S') if task.completed_time else None,
                    'student_status': student.status,
                    'student_status_display': student.get_status_display()
                }
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except RegistrationTask.DoesNotExist:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': '未找到该任务'
            }, ensure_ascii=False),
            content_type='application/json',
            status=404
        )
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    """智能问答接口"""
    try:
        # 获取用户问题
        question = request.POST.get('question')
        
        if not question:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '请输入问题'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 简单的问答逻辑
        # 这里可以集成更复杂的AI模型
        answers = {
            '宿舍几点关门': '根据学校规定，宿舍通常在晚上11点关门。',
            '宿舍几点断电': '周日至周四晚 23:00 断电断网，周五、周六及节假日通宵供电。',
            '食堂好吃吗': '学校共有 3 个食堂。一食堂便宜量大（人均 8-12 元）；二食堂风味多（人均 12-20 元）；三食堂有空调和小炒。',
            '校园网怎么连接': '连接 Campus-WiFi 信号，账号为学号，初始密码为身份证后六位。',
            '学费忘记交了怎么办': '不要急，报到现场设有"绿色通道"，可以先办理入学手续，后续补交或办理助学贷款。',
            '军训要站多久': '每天训练时间通常为上午 8:00-11:30，下午 14:30-17:30，晚上可能有拉歌或内务整理。',
            '大一可以带电脑吗': '可以带。但大一上学期通常不允许参加英语四级考试（视具体学院规定），电脑主要用于查阅资料和完成作业。',
            '转专业难不难': '通常在大一下学期开放申请。要求大一第一学期绩点排名专业前 10%-20%，且无挂科记录，需通过转入学院的面试。',
            '图书馆怎么借书': '凭校园卡（或电子校园码）进入。每人可借 10 本，借期 30 天，可续借一次。',
            '体育课选什么好过': '建议避开对体能要求极高的项目（如长跑）。瑜伽、太极、乒乓球通常比较热门。'
        }
        
        # 查找匹配的答案
        answer = answers.get(question, '您好！关于您的问题，我正在查询相关信息。如果您有其他问题，随时可以向我咨询。')
        
        # 也可以基于FAQ数据进行匹配
        import re
        faqs = FAQ.objects.all()
        for faq in faqs:
            if re.search(question, faq.title) or re.search(question, faq.content):
                answer = faq.answer
                break
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'data': {
                    'question': question,
                    'answer': answer
                }
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@require_http_methods(["GET"])
def admin_dashboard(request):
    """管理端仪表盘接口"""
    try:
        # 获取筛选参数
        college = request.GET.get('college')
        major = request.GET.get('major')
        status = request.GET.get('status')
        search = request.GET.get('search')
        
        # 构建查询
        query = Student.objects.all()
        
        # 应用筛选
        if college:
            query = query.filter(college=college)
        if major:
            query = query.filter(major=major)
        if status:
            query = query.filter(status=status)
        if search:
            query = query.filter(models.Q(student_id__icontains=search) | models.Q(name__icontains=search))
        
        # 统计数据
        total_count = Student.objects.count()
        completed_count = Student.objects.filter(status='COMPLETED').count()
        in_progress_count = Student.objects.filter(status='IN_PROGRESS').count()
        unregistered_count = Student.objects.filter(status='UNREGISTERED').count()
        
        # 计算报到率
        registration_rate = (completed_count / total_count * 100) if total_count > 0 else 0
        
        # 获取学生列表
        students = []
        for student in query:
            # 获取学生的任务状态
            tasks = RegistrationTask.objects.filter(student=student)
            task_status = {}
            for task in tasks:
                task_status[task.task_name] = task.status == 'COMPLETED'
            
            # 根据任务状态重新计算总体状态，确保与任务状态一致
            completed_tasks = tasks.filter(status='COMPLETED')
            if completed_tasks.count() == tasks.count() and tasks.count() > 0:
                # 所有任务都已完成
                current_status = 'COMPLETED'
                status_display = '已完成'
            elif completed_tasks.count() > 0:
                # 部分任务已完成
                current_status = 'IN_PROGRESS'
                status_display = '进行中'
            else:
                # 没有任务完成
                current_status = 'UNREGISTERED'
                status_display = '未报到'
            
            student_data = {
                'student_id': student.student_id,
                'name': student.name,
                'college': student.college,
                'major': student.major,
                'phone': student.phone,
                'status': current_status,
                'status_display': status_display,
                'task_status': task_status
            }
            students.append(student_data)
        
        # 获取学院和专业列表（用于筛选）
        colleges = Student.objects.values_list('college', flat=True).distinct()
        majors = Student.objects.values_list('major', flat=True).distinct()
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'data': {
                    'stats': {
                        'total_count': total_count,
                        'completed_count': completed_count,
                        'in_progress_count': in_progress_count,
                        'unregistered_count': unregistered_count,
                        'registration_rate': round(registration_rate, 2)
                    },
                    'students': students,
                    'filters': {
                        'colleges': list(colleges),
                        'majors': list(majors)
                    }
                }
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def force_complete(request):
    """强制通过学生报到"""
    try:
        student_id = request.POST.get('student_id')
        
        if not student_id:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '请提供学生学号'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 查找学生
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '学生不存在'
                }, ensure_ascii=False),
                content_type='application/json',
                status=404
            )
        
        # 将所有任务标记为已完成
        tasks = RegistrationTask.objects.filter(student=student)
        for task in tasks:
            task.status = 'COMPLETED'
            from django.utils import timezone
            task.completed_time = timezone.now()
            task.save()
        
        # 更新学生状态为已完成
        student.status = 'COMPLETED'
        student.save()
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'message': '已成功强制通过学生报到'
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@require_http_methods(["GET"])
def get_student_detail(request):
    """获取学生详情"""
    try:
        student_id = request.GET.get('student_id')
        
        if not student_id:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '请提供学生学号'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 查找学生
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '学生不存在'
                }, ensure_ascii=False),
                content_type='application/json',
                status=404
            )
        
        # 获取学生的任务状态
        tasks = RegistrationTask.objects.filter(student=student)
        task_list = []
        for task in tasks:
            task_list.append({
                'task_name': task.task_name,
                'status': task.status,
                'status_display': '已完成' if task.status == 'COMPLETED' else '未完成',
                'completed_time': task.completed_time.strftime('%Y-%m-%d %H:%M:%S') if task.completed_time else None
            })
        
        # 构建学生详情数据
        student_detail = {
            'student_id': student.student_id,
            'name': student.name,
            'id_card': student.id_card,
            'major': student.major,
            'college': student.college,
            'phone': student.phone,
            'status': student.status,
            'status_display': student.get_status_display(),
            'created_at': student.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': student.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'tasks': task_list
        }
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'data': student_detail
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """新生注册接口"""
    try:
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        id_card = request.POST.get('id_card')
        major = request.POST.get('major')
        college = request.POST.get('college')
        phone = request.POST.get('phone')
        
        # 验证必填字段
        if not all([student_id, name, id_card, major, college, phone]):
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '请填写所有必填字段'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 检查学号是否已存在
        if Student.objects.filter(student_id=student_id).exists():
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '学号已存在'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 检查身份证号是否已存在
        if Student.objects.filter(id_card=id_card).exists():
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '身份证号已存在'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 创建学生记录
        student = Student(
            student_id=student_id,
            name=name,
            id_card=id_card,
            major=major,
            college=college,
            phone=phone,
            status='UNREGISTERED'
        )
        student.save()
        
        # 为新学生分配默认任务
        default_tasks = ['缴纳学费', '宿舍入住办理', '领取军训物资', '到校登记', '填写个人信息']
        for task_name in default_tasks:
            RegistrationTask(
                student=student,
                task_name=task_name,
                status='PENDING'
            ).save()
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'message': '注册成功'
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def update_student_info(request):
    """更新学生个人信息"""
    try:
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        id_card = request.POST.get('id_card')
        phone = request.POST.get('phone')
        college = request.POST.get('college')
        major = request.POST.get('major')
        
        # 验证必填字段
        if not all([student_id, name, id_card, phone, college, major]):
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '请填写所有必填字段'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 查找学生
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '学生不存在'
                }, ensure_ascii=False),
                content_type='application/json',
                status=404
            )
        
        # 检查身份证号是否被其他学生使用
        if Student.objects.filter(id_card=id_card).exclude(student_id=student_id).exists():
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '身份证号已被其他学生使用'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 更新学生信息
        student.name = name
        student.id_card = id_card
        student.phone = phone
        student.college = college
        student.major = major
        student.save()
        
        # 标记"填写个人信息"任务为已完成
        try:
            task = RegistrationTask.objects.get(student=student, task_name='填写个人信息')
            task.status = 'COMPLETED'
            from django.utils import timezone
            task.completed_time = timezone.now()
            task.save()
        except RegistrationTask.DoesNotExist:
            pass
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'message': '信息更新成功'
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def arrival_register(request):
    """到校登记接口"""
    try:
        student_id = request.POST.get('student_id')
        arrival_date = request.POST.get('arrival_date')
        arrival_time = request.POST.get('arrival_time')
        transportation = request.POST.get('transportation')
        contact_person = request.POST.get('contact_person')
        contact_phone = request.POST.get('contact_phone')
        
        # 验证必填字段
        if not all([student_id, arrival_date, arrival_time, transportation, contact_person, contact_phone]):
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '请填写所有必填字段'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 查找学生
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '学生不存在'
                }, ensure_ascii=False),
                content_type='application/json',
                status=404
            )
        
        # 标记"到校登记"任务为已完成
        try:
            task = RegistrationTask.objects.get(student=student, task_name='到校登记')
            task.status = 'COMPLETED'
            from django.utils import timezone
            task.completed_time = timezone.now()
            task.save()
        except RegistrationTask.DoesNotExist:
            pass
        
        # 更新学生状态为进行中（如果当前是未报到状态）
        if student.status == 'UNREGISTERED':
            student.status = 'IN_PROGRESS'
            student.save()
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'message': '到校登记成功'
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def dorm_select(request):
    """宿舍选择接口"""
    try:
        student_id = request.POST.get('student_id')
        building = request.POST.get('building')
        room = request.POST.get('room')
        
        # 验证必填字段
        if not all([student_id, building, room]):
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '请填写所有必填字段'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 查找学生
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '学生不存在'
                }, ensure_ascii=False),
                content_type='application/json',
                status=404
            )
        
        # 检查学生是否已分配宿舍
        if hasattr(student, 'dormitory') and student.dormitory:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '您已分配宿舍，不能重复选择'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 查找或创建宿舍
        dorm, created = Dormitory.objects.get_or_create(
            building=building,
            room=room,
            defaults={
                'total_beds': 4,
                'available_beds': 4,
                'is_occupied': False
            }
        )
        
        # 检查宿舍是否已满
        if dorm.available_beds <= 0:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '该宿舍已满，请选择其他宿舍'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 分配宿舍给学生
        StudentDormitory.objects.create(
            student=student,
            dormitory=dorm
        )
        
        # 更新宿舍剩余床位
        dorm.available_beds -= 1
        if dorm.available_beds == 0:
            dorm.is_occupied = True
        dorm.save()
        
        # 标记"宿舍入住办理"任务为已完成
        try:
            task = RegistrationTask.objects.get(student=student, task_name='宿舍入住办理')
            task.status = 'COMPLETED'
            from django.utils import timezone
            task.completed_time = timezone.now()
            task.save()
        except RegistrationTask.DoesNotExist:
            pass
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'message': '宿舍选择成功'
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def admin_edit_student(request):
    """管理员编辑学生信息接口"""
    try:
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        id_card = request.POST.get('id_card')
        major = request.POST.get('major')
        college = request.POST.get('college')
        phone = request.POST.get('phone')
        status = request.POST.get('status')
        
        # 验证必填字段
        if not all([student_id, name, id_card, major, college, phone, status]):
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '请填写所有必填字段'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 查找学生
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '学生不存在'
                }, ensure_ascii=False),
                content_type='application/json',
                status=404
            )
        
        # 检查身份证号是否被其他学生使用
        if Student.objects.filter(id_card=id_card).exclude(student_id=student_id).exists():
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '身份证号已被其他学生使用'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 更新学生信息
        student.name = name
        student.id_card = id_card
        student.major = major
        student.college = college
        student.phone = phone
        student.status = status
        student.save()
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'message': '学生信息编辑成功'
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@require_http_methods(["GET"])
def get_dorms(request):
    """获取宿舍列表"""
    try:
        # 获取查询参数
        building = request.GET.get('building')
        status = request.GET.get('status')
        room = request.GET.get('room')
        
        # 构建查询
        query = Dormitory.objects.all()
        
        if building:
            query = query.filter(building=building)
        
        if status == 'available':
            query = query.filter(available_beds__gt=0)
        elif status == 'full':
            query = query.filter(available_beds=0)
        
        if room:
            query = query.filter(room__contains=room)
        
        # 获取所有宿舍楼
        buildings = Dormitory.objects.values_list('building', flat=True).distinct()
        
        # 构建宿舍数据
        dorm_list = []
        for dorm in query:
            dorm_list.append({
                'id': dorm.id,
                'building': dorm.building,
                'room': dorm.room,
                'total_beds': dorm.total_beds,
                'available_beds': dorm.available_beds,
                'is_occupied': dorm.is_occupied
            })
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'data': {
                    'dorms': dorm_list,
                    'buildings': list(buildings)
                }
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@require_http_methods(["GET"])
def get_dorm_detail(request):
    """获取宿舍详情"""
    try:
        dorm_id = request.GET.get('dorm_id')
        
        if not dorm_id:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '请提供宿舍ID'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        try:
            dorm = Dormitory.objects.get(id=dorm_id)
        except Dormitory.DoesNotExist:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '宿舍不存在'
                }, ensure_ascii=False),
                content_type='application/json',
                status=404
            )
        
        dorm_detail = {
            'id': dorm.id,
            'building': dorm.building,
            'room': dorm.room,
            'total_beds': dorm.total_beds,
            'available_beds': dorm.available_beds,
            'is_occupied': dorm.is_occupied
        }
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'data': dorm_detail
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def save_dorm(request):
    """保存宿舍信息（添加或编辑）"""
    try:
        dorm_id = request.POST.get('dorm_id')
        building = request.POST.get('building')
        room = request.POST.get('room')
        total_beds = request.POST.get('total_beds')
        available_beds = request.POST.get('available_beds')
        
        # 验证必填字段
        if not all([building, room, total_beds, available_beds]):
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '请填写所有必填字段'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 转换数据类型
        total_beds = int(total_beds)
        available_beds = int(available_beds)
        
        # 验证数据有效性
        if total_beds < 1:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '总床位必须大于0'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        if available_beds < 0 or available_beds > total_beds:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '剩余床位必须在0到总床位之间'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 检查宿舍是否已存在
        existing_dorm = Dormitory.objects.filter(building=building, room=room)
        if dorm_id:
            existing_dorm = existing_dorm.exclude(id=dorm_id)
        
        if existing_dorm.exists():
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': '该宿舍已存在'
                }, ensure_ascii=False),
                content_type='application/json',
                status=400
            )
        
        # 保存宿舍信息
        if dorm_id:
            # 编辑现有宿舍
            try:
                dorm = Dormitory.objects.get(id=dorm_id)
                dorm.building = building
                dorm.room = room
                dorm.total_beds = total_beds
                dorm.available_beds = available_beds
                dorm.is_occupied = (available_beds == 0)
                dorm.save()
            except Dormitory.DoesNotExist:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': '宿舍不存在'
                    }, ensure_ascii=False),
                    content_type='application/json',
                    status=404
                )
        else:
            # 添加新宿舍
            Dormitory.objects.create(
                building=building,
                room=room,
                total_beds=total_beds,
                available_beds=available_beds,
                is_occupied=(available_beds == 0)
            )
        
        return HttpResponse(
            json.dumps({
                'success': True,
                'message': '操作成功'
            }, ensure_ascii=False),
            content_type='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, ensure_ascii=False),
            content_type='application/json',
            status=500
        )