# 使用 Miniconda 基础镜像
FROM continuumio/miniconda3

# 设置工作目录为 /app
WORKDIR /app

# 将主机项目文件复制到容器中的 /app
COPY . /app

# 设置 Conda 使用国内镜像源并创建环境、安装依赖
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free && \
    conda config --set show_channel_urls yes && \
    conda create -n flask_env python=3.9 -y --override-channels -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free && \
    echo "source activate flask_env" > ~/.bashrc && \
    /bin/bash -c "source activate flask_env && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt"

# 暴露端口
EXPOSE 5010

# 启动 Flask 应用，使用 flask_env 环境
CMD ["bash", "-c", "source ~/.bashrc && source activate flask_env && python run.py"]
