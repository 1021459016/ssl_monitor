# 使用官方Python基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

RUN apt-get update && apt-get install -y curl vim
# 复制项目文件
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 启动命令
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]