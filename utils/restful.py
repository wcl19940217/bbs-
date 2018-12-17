from flask import jsonify


class HttpCode(object):
    ok = 200
    unautherror = 401
    paramserror = 400
    servererror = 500


def restful_result(code, message, data):
    return jsonify({'code': code, 'message': message, 'data': data or {}})


def success(message="", data=""):
    return restful_result(code=HttpCode.ok, message=message, data=data)


def unauth_error(message="", data=""):
    return restful_result(code=HttpCode.unautherror, message=message, data=data)


def paramerror(message="", data=""):
    return restful_result(code=HttpCode.paramserror, message=message, data=data)


def servererror(message="", data=""):
    return restful_result(code=HttpCode.servererror, message=message, data=data)