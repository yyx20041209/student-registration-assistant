# 大学生新生报到智能助手

一个完整的大学新生报到管理系统，包含学生端和管理员端功能，提供报到流程指导、信息管理、宿舍选择和智能问答等功能。

## 功能特性

### 学生端功能

1. **新生注册**
   - 学号、姓名、身份证号验证
   - 个人信息填写和提交

2. **报到任务管理**
   - 查看报到任务列表
   - 任务状态更新和进度跟踪
   - 任务完成确认

3. **个人信息管理**
   - 查看个人基本信息
   - 编辑和更新个人信息
   - 信息验证和保存

4. **到校登记**
   - 记录到校时间和方式
   - 报到确认

5. **宿舍选择**
   - 查看可用宿舍列表
   - 选择心仪的宿舍
   - 宿舍分配确认

6. **校园地图**
   - 交互式校园地图
   - 支持选择学校（青岛大学、山东大学等）
   - 校园建筑列表展示
   - 一键跳转高德地图导航
   - 建筑信息和导航
   - 地点详情查看

7. **智能问答**
   - 基于关键词的智能问答
   - 常见问题自动回复
   - 友好的聊天界面

8. **常见问题（FAQ）**
   - 分类展示常见问题
   - 详细的问题解答
   - 快速查找功能

### 管理员端功能

1. **报到总览**
   - 学生报到统计数据
   - 各学院报到情况
   - 实时状态监控

2. **学生管理**
   - 学生列表查看
   - 学生详情编辑
   - 强制完成报到

3. **宿舍管理**
   - 宿舍信息管理
   - 床位状态更新
   - 宿舍分配管理

4. **数据筛选**
   - 按学院、专业筛选
   - 按报到状态筛选
   - 学号和姓名搜索

## 技术实现

### 后端技术
- **框架**：Django 6.0.4
- **数据库**：SQLite（支持迁移到MySQL）
- **API设计**：RESTful API
- **ORM**：Django ORM

### 前端技术
- **基础技术**：HTML5, CSS3, JavaScript
- **响应式设计**：适配PC和移动端
- **交互方式**：AJAX + Fetch API
- **用户界面**：现代化的卡片式布局，渐变色彩

### 系统架构
- **前后端分离**：前端静态页面 + 后端API
- **API接口**：统一的JSON响应格式
- **数据存储**：SQLite数据库
- **部署方式**：Django开发服务器

## 项目结构

```
student-registration-assistant/
├── myapp/                      # Django应用目录
│   ├── __init__.py            # Python包初始化
│   ├── models.py              # 数据模型定义
│   ├── views.py               # 视图函数
│   ├── urls.py                # URL路由配置
│   ├── admin.py               # Django Admin配置
│   └── migrations/            # 数据库迁移文件
├── registration_assistant/     # Django项目配置
│   ├── __init__.py
│   ├── settings.py            # 项目配置文件
│   ├── urls.py                # 主URL路由
│   ├── wsgi.py                # WSGI配置
│   └── asgi.py                # ASGI配置
├── static/                    # 静态文件目录
│   ├── login-select.html      # 登录选择页面
│   ├── login.html             # 学生登录页面
│   ├── admin-login.html        # 管理员登录页面
│   ├── index.html             # 学生主页面
│   ├── profile.html           # 个人信息页面
│   ├── arrival.html           # 到校登记页面
│   ├── dorm-select.html       # 宿舍选择页面
│   ├── campus-map-simple.html  # 校园地图页面（高德导航版）
│   ├── campus-map-amap.html    # 校园地图页面（高德增强版）
│   ├── campus-map-real.html    # 校园地图页面（实时搜索版）
│   ├── campus-map.html         # 校园地图页面（静态版）
│   ├── admin.html             # 管理员主页面
│   └── dorm-management.html  # 宿舍管理页面
├── media/                     # 媒体文件目录
├── db.sqlite3                 # SQLite数据库文件
├── manage.py                  # Django管理命令
├── add_dorm_data.py           # 宿舍数据添加脚本
├── 技术方案.md                 # 技术方案文档
└── README.md                  # 项目说明文档
```

## 快速开始

### 环境要求
- Python 3.8+
- Django 6.0.4

### 安装和运行

1. **安装依赖**
   ```bash
   pip install Django
   ```

2. **数据库迁移**
   ```bash
   python manage.py migrate
   ```

3. **添加测试数据**
   ```bash
   python add_dorm_data.py
   ```

4. **启动开发服务器**
   ```bash
   python manage.py runserver 8000
   ```

5. **访问系统**
   - 打开浏览器，访问 `http://localhost:8000/static/login-select.html`
   - 选择"学生端"或"管理员端"登录
   - 学生端：使用测试学号登录（如20260201）
   - 管理员端：直接登录（无需账号密码）

## API接口

### 学生端接口
- `POST /api/student/register/` - 学生注册
- `GET /api/student/info/` - 获取学生信息
- `POST /api/student/update/` - 更新学生信息
- `GET /api/student/tasks/` - 获取任务列表
- `POST /api/student/arrival/` - 到校登记
- `POST /api/student/dorm-select/` - 宿舍选择

### 管理端接口
- `GET /api/admin/dashboard/` - 获取仪表盘数据
- `GET /api/admin/student-detail/` - 获取学生详情
- `POST /api/admin/edit-student/` - 编辑学生信息
- `POST /api/admin/force-complete/` - 强制完成报到
- `GET /api/admin/dorms/` - 获取宿舍列表
- `GET /api/admin/dorm-detail/` - 获取宿舍详情
- `POST /api/admin/save-dorm/` - 保存宿舍信息

### 共享接口
- `GET /api/faqs/` - 获取常见问题
- `POST /api/task/update/` - 更新任务状态
- `POST /api/chat/` - 智能问答

## 技术方案

详细的技术实现方案请参考 [技术方案.md](技术方案.md) 文件。

## 测试数据

系统中已包含以下测试数据：

### 学生数据
- 学号：20260201-20260501
- 覆盖不同学院和专业
- 包含不同报到状态

### 宿舍数据
- 1号楼：101、102、103、104房间
- 2号楼：201、202、203房间
- 3号楼：301、302房间
- 4号楼：401房间

### 常见问题
- 分类涵盖：宿舍生活、饮食、校园网、快递、学习、学籍管理、图书馆、体育课、军训、财务、报到流程

## 未来扩展

- **数据库升级**：迁移到MySQL数据库
- **用户认证**：实现JWT token认证系统
- **通知系统**：添加短信/邮件通知功能
- **数据分析**：实现报到数据统计和分析
- **移动应用**：开发配套的移动应用
- **AI增强**：集成更先进的智能问答系统

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License

## 联系方式

- GitHub：https://github.com/yyx20041209/freshman-registration
- 项目维护：yyx20041209
