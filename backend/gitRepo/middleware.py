# middleware.py

from .models import UserAction
import json

class UserActionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 在请求处理之前读取并存储请求体的数据
        payload = None
        if request.method in ['POST','PATCH'] and request.content_type == 'application/json':
            payload = json.loads(request.body.decode('utf-8'))
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.method == 'POST':
                try:
                    if request.content_type == 'application/json':
                        payload = payload.get('Name')
                    else:
                        payload = request.POST.get('Name')
                except Exception as e:
                    payload = str(e)  # 如果解析出错，存储错误信息
            elif request.method == 'PATCH':
                try:
                    if request.content_type == 'application/json':
                        payload = payload.get('Name')
                    else:
                        payload = request.POST.get('Name')
                except Exception as e:
                    payload = str(e)  # 如果解析出错，存储错误信息
            # delete 在delelte函数中单独处理
            UserAction.objects.create(
                user=request.user,
                action=f"Accessed {request.path}",
                method=request.method,
                status_code=response.status_code,
                payload=payload
            )

        return response