from rest_framework import serializers
from .models import Repository
from django.contrib.auth.models import User


class RepositorySerializer(serializers.ModelSerializer):
    # 手动添加Username字段
    username = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Repository
        fields = '__all__'

    def create(self, validated_data):
        print(1)
        username = validated_data.pop('username', None)
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError(f'User with username {username} does not exist')
            validated_data['Owner'] = user
        else:
            raise serializers.ValidationError('Username is required')

        return super().create(validated_data)
