from flask import Flask
from dotenv import load_dotenv

# 加载 .env 文件,读取项目根目录下的.env文件，将文件中定义的环境变量加载到系统环境中，通过os.getenv等方法访问变量
load_dotenv()

#配置好Flask应用实例
def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

   #从view.py导入蓝图对象，用于管理应用路由
    from app.views import bp as views_bp
    # 将蓝图注册到Flask应用中，将不同模块的路径和逻辑分离到各自文件中，有助于代码的组织和可维护性
    app.register_blueprint(views_bp)

    return app
