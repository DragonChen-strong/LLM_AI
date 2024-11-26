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
    conda create -n flask_env python=3.9 -y --override-channels -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free && \
    /bin/bash -c "source activate flask_env && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt"



# 安装 fontconfig 以支持 fc-cache
RUN apt-get update && \
         apt-get install -y fontconfig && \
         fc-cache -fv


# 添加 PYTHONPATH 环境变量
ENV PYTHONPATH="/app/module:${PYTHONPATH}"
ENV PYTHONUNBUFFERED=1




# 设置默认运行命令，使用 `conda run` 保证环境激活
CMD ["conda", "run", "-n", "flask_env", "python", "app.py"]
