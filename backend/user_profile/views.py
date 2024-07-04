from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ProfileSerializer
from .models import UserProfile, validate_image
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your views here.
@api_view(['GET', 'PATCH', 'POST'])
def profile(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)

    if user is None:
        return JsonResponse({'error': 'Invalid token'}, status=401)

        # 假设用户已经通过身份验证，现在可以获取用户的配置信息
    if request.method == 'GET':
        try:
            # 获取用户的所有仓库
            user_profile = ProfileSerializer(user.profile)
            print(user_profile.data)
            return JsonResponse(user_profile.data, safe=False)

        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=404)

    #
    elif request.method == 'POST':  #
        try:
            # 创建一个新的配置信息
            profile_data = request.data
            new_profile_data = {'name' : user.username,
                                'email': profile_data['email'],
                                'description': profile_data['description'],
                                'link': profile_data['Link'],
                                'Owner': user.pk}
            # 为repo_data添加一个Owner字段,但是由于他是QueryDick类型，所以不能直接添加
            # print(repo_data)
            profile_serializer = ProfileSerializer(data=new_profile_data)

            if profile_serializer.is_valid():
                profile_serializer.save()
                return JsonResponse(profile_serializer.data, status=201)

            return JsonResponse(profile_serializer.errors, status=400)

        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'PATCH':
        try:
            # 更新用户的配置信息
            profile_data = request.data
            print(profile_data)

            if "name" in profile_data or "Owner" in profile_data or 'avatar' in profile_data:
                # 如果请求中包含id或owner字段，则返回不能请求
                return JsonResponse({'error': 'Cannot update name or owner or avatar fields'}, status=400)

            # 为repo_data添加一个Owner字段,但是由于他是QueryDick类型，所以不能直接添加
            # print(repo_data)
            profile_serializer = ProfileSerializer(user.profile, data=profile_data, partial=True)

            if profile_serializer.is_valid():
                profile_serializer.save()
                return JsonResponse(profile_serializer.data, status=201)

            return JsonResponse(profile_serializer.errors, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# 上传头像
@api_view(['POST'])
def upload_avatar(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)

    if user is None:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    try:
        if request.method == 'POST':
            avatar = request.FILES['avatar']
            # print(avatar.content_type)
            # 确保文件是一个有效的图像文件
            if not validate_image(avatar):
                return JsonResponse({'status': 'error', 'message': 'Invalid image file.'}, status=400)

            user_profile = user.profile
            # 更新用户资料中的头像
            user_profile.avatar = avatar
            user_profile.save()

            # 返回成功的响应
            return JsonResponse({'status': 'success', 'message': 'Avatar uploaded successfully.'})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)

    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)