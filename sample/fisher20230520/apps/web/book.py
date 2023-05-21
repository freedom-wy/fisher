from flask import jsonify, make_response, Blueprint
from apps.web.blueprint import web


@web.route("/api")
def api():
    # 通过make_response封装返回, 通过jsonify封装数据
    return make_response(jsonify({"msg": "ok"}), 404)


@web.route("/test")
def test():
    return "test"
