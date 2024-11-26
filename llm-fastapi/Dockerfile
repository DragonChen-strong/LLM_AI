# 使用 Miniconda 基础镜像
FROM continuumio/miniconda3

# 设置工作目录
WORKDIR /app

# 复制项目文件到工作目录
COPY . /app

# 配置国内镜像源，并创建新的 Conda 环境
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free && \
    conda config --set show_channel_urls yes && \
    conda create -n weather_env python=3.9 -y --override-channels -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free && \
    /bin/bash -c "source activate weather_env && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt"

# 复制模型文件到镜像中
COPY zh_core_web_sm-3.8.0.tar.gz /app/

# 安装本地模型
RUN /bin/bash -c "source activate weather_env && pip install /app/zh_core_web_sm-3.8.0.tar.gz"

# 暴露端口
EXPOSE 7502

# 设置默认运行命令，使用 `conda run` 保证环境激活
CMD ["conda", "run", "-n", "weather_env", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7502"]

