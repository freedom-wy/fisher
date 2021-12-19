# 解决循环导入问题
from flask import Blueprint

book_bp = Blueprint("book_bp", __name__)
