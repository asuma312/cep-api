import functools
from flask import session, redirect, url_for, g,request,jsonify
from functools import wraps
from models.db import USER,CEP



def verify_apikey(route):
    @wraps(route)
    def decorated_function(*args, **kwargs):
        headers = request.headers
        apikey = headers.get("apikey")
        user = USER.query.filter_by(apikey=apikey).first()
        if not user:
            return jsonify({"message":"APIKEY inválida"}),401

        g.user = user
        ceps = CEP.query.filter_by(usuario_id=user.user_hash).all()
        g.ceps = ceps

        return route(*args, **kwargs)

    return decorated_function
