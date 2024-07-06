from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ConfigSerializer
from .models import UserConfig
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your views here.
@api_view(['GET', 'PATCH', 'POST'])
def config(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)

    if user is None:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    # 假设用户已经通过身份验证，现在可以获取用户的配置信息
    if request.method == 'GET':
        try:
            # 获取用户的配置信息
            user_config = ConfigSerializer(user.config)
            return JsonResponse(user_config.data, safe=False)

        except UserConfig.DoesNotExist:
            return JsonResponse({'error': 'User config not found'}, status=404)

    #
    elif request.method == 'POST':
        try:
            # 创建一个新的配置信息
            config_data = request.data
            new_config_data = {'app_id': config_data['app_id'],
                                'api_secret': config_data['api_secret'],
                                'api_key': config_data['api_key'],
                                'version': config_data['version'],
                                'max_tokens': config_data['max_tokens'],
                                'temperature': config_data['temperature'],
                                'owner': user.pk}
            # 为repo_data添加一个Owner字段,但是由于他是QueryDick类型，所以不能直接添加
            config_serializer = ConfigSerializer(data=new_config_data)

            if config_serializer.is_valid():
                config_serializer.save()
                return JsonResponse(config_serializer.data, status=201)

            return JsonResponse(config_serializer.errors, status=400)

        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    elif request.method == 'PATCH':
        try:
            # 更新用户的配置信息
            config_data = request.data
            print(config_data)

            if "owner" in config_data:
                # 如果请求中包含owner字段，则返回不能请求
                return JsonResponse({'error': 'Cannot update owner field'}, status=400)

            # 为repo_data添加一个Owner字段,但是由于他是QueryDick类型，所以不能直接添加
            # print(repo_data)
            config_serializer = ConfigSerializer(user.config, data=config_data, partial=True)

            if config_serializer.is_valid():
                config_serializer.save()
                return JsonResponse(config_serializer.data, status=201)

            return JsonResponse(config_serializer.errors, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)