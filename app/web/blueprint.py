# 解决循环导入问题
from flask import Blueprint

# 蓝图中也可以指定蓝图自己的静态资源目录和URL
book_bp = Blueprint("book_bp", __name__, template_folder="templates")
