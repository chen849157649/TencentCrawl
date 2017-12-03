from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
app = Celery('celery_tasks.tasks', backend='redis://localhost:6379/2', broker='redis://localhost:6379/1')
# @app.task
# def my_task(a, b):
#     print('任务函数正在执行')
#     return a + b


@app.task
def send_active_email(token, username, email):
    subject = '天天生鲜邮箱验证'
    message = ''
    from_email = settings.EMAIL_FROM
    recipient_list = [email]
    html_message = '<a href="http://127.0.0.1:8000/user/active/%s/">请点击链接激活账号http://127.0.0.1:8000/user/active/</a>' % token
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)