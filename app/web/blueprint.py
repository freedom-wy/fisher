# 解决循环导入问题
from flask import Blueprint, render_template

# 蓝图中也可以指定蓝图自己的静态资源目录和URL
# book_bp = Blueprint("book_bp", __name__, template_folder="templates")
web = Blueprint("web", __name__)


# # 用于规范输出404页面,AOP编程思想
# @web.app_errorhandler(404)
# def not_found(e):
#     return render_template("404.html"), 404
