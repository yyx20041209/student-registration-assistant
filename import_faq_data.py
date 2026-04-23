#!/usr/bin/env python3
"""
批量导入常见问题数据到数据库
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registration_assistant.settings')
django.setup()

from myapp.models import FAQ

# 常见问题数据
faq_data = [
    # 生活篇
    {
        'title': '宿舍几点断电/断网？',
        'content': '宿舍几点断电/断网？',
        'answer': '周日至周四晚 23:00 断电断网，周五、周六及节假日通宵供电。空调插座通常不断电。',
        'category': 'LIFE'
    },
    {
        'title': '宿舍限电功率是多少？',
        'content': '宿舍限电功率是多少？',
        'answer': '宿舍限制大功率电器，通常限制在 800W-1000W 以内。吹风机、电磁炉、热得快严禁使用，否则会跳闸并通报。',
        'category': 'LIFE'
    },
    {
        'title': '食堂好吃吗？贵不贵？',
        'content': '食堂好吃吗？贵不贵？',
        'answer': '学校共有 3 个食堂。一食堂便宜量大（人均 8-12 元）；二食堂风味多（人均 12-20 元）；三食堂有空调和小炒。支持微信/支付宝/校园卡支付。',
        'category': 'LIFE'
    },
    {
        'title': '校园网怎么连接？',
        'content': '校园网怎么连接？',
        'answer': '连接 Campus-WiFi 信号，账号为学号，初始密码为身份证后六位。首次登录需在弹窗页面下载认证客户端。',
        'category': 'LIFE'
    },
    {
        'title': '快递地址怎么填？',
        'content': '快递地址怎么填？',
        'answer': '地址：xx省xx市xx区xx路xx号 [你的大学名称]。取件点：南区在菜鸟驿站，北区在近邻宝。',
        'category': 'LIFE'
    },
    # 学业篇
    {
        'title': '大一可以带电脑吗？',
        'content': '大一可以带电脑吗？',
        'answer': '可以带。但大一上学期通常不允许参加英语四级考试（视具体学院规定），电脑主要用于查阅资料和完成作业。',
        'category': 'TEACHING'
    },
    {
        'title': '转专业难不难？',
        'content': '转专业难不难？',
        'answer': '通常在大一下学期开放申请。要求大一第一学期绩点排名专业前 10%-20%，且无挂科记录，需通过转入学院的面试。',
        'category': 'TEACHING'
    },
    {
        'title': '图书馆怎么借书？',
        'content': '图书馆怎么借书？',
        'answer': '凭校园卡（或电子校园码）进入。每人可借 10 本，借期 30 天，可续借一次。',
        'category': 'TEACHING'
    },
    {
        'title': '体育课选什么好过？',
        'content': '体育课选什么好过？',
        'answer': '建议避开对体能要求极高的项目（如长跑）。瑜伽、太极、乒乓球通常比较热门，建议选课系统开放时“秒杀”。',
        'category': 'TEACHING'
    },
    # 报到与军训篇
    {
        'title': '军训要站多久？',
        'content': '军训要站多久？',
        'answer': '每天训练时间通常为上午 8:00-11:30，下午 14:30-17:30，晚上可能有拉歌或内务整理。中间有休息时间。',
        'category': 'REGISTRATION'
    },
    {
        'title': '军训必须买学校的鞋吗？',
        'content': '军训必须买学校的鞋吗？',
        'answer': '建议买，但可以买大两码，并在鞋垫下垫卫生巾（这是学长学姐的秘诀，非常吸汗减震）。',
        'category': 'REGISTRATION'
    },
    {
        'title': '学费忘记交了怎么办？',
        'content': '学费忘记交了怎么办？',
        'answer': '不要急，报到现场设有“绿色通道”，可以先办理入学手续，后续补交或办理助学贷款。',
        'category': 'REGISTRATION'
    },
    {
        'title': '报到那天家长能进宿舍吗？',
        'content': '报到那天家长能进宿舍吗？',
        'answer': '可以。学校设有志愿者服务点，家长可协助将行李搬运至宿舍楼下。',
        'category': 'REGISTRATION'
    }
]

def import_faq_data():
    """批量导入FAQ数据"""
    print("开始导入FAQ数据...")
    
    # 清空现有数据（可选）
    # FAQ.objects.all().delete()
    # print("已清空现有FAQ数据")
    
    # 导入新数据
    created_count = 0
    for item in faq_data:
        # 检查是否已存在
        if not FAQ.objects.filter(title=item['title']).exists():
            FAQ.objects.create(**item)
            created_count += 1
            print(f"已导入: {item['title']}")
        else:
            print(f"跳过（已存在）: {item['title']}")
    
    print(f"\n导入完成！共导入 {created_count} 条新数据")
    print(f"当前数据库中共有 {FAQ.objects.count()} 条FAQ数据")

if __name__ == "__main__":
    import_faq_data()