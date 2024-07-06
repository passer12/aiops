# 使用官方的 Python 镜像作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /usr/src/app

# 复制 requirements.txt 文件到工作目录
COPY requirements.txt ./

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件到工作目录
COPY . .

# 运行 Django 迁移和启动服务
EXPOSE 8000
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
