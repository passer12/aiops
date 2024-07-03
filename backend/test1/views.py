from django.http import JsonResponse
from django.shortcuts import render, HttpResponse


# Create your views here.
def test1(request):
    # 测试接口
    test1_data = {'message': 'hello django'}
    return JsonResponse(test1_data)
