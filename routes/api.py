from flask import Blueprint, jsonify, request, g,current_app
from models.db import USER, CEP, db
from models.data_models import CEP_MODEL
from utils.logger import log_request, log_exception, log_db_operation
from utils.decorators import verify_apikey
from typing import Union, Dict, Optional
from utils.cache import cache_controller

blueprint: Blueprint = Blueprint('api', __name__)

def get_from_cache(cep: str) -> Union[None, Dict]:
    cache = cache_controller()
    is_created: bool = cache.verify_create_json(cep, {})
    if is_created:
        return None
    return cache.get_json(cep)

def get_write_from_cache(cep:str, cep_obj:CEP)->CEP_MODEL:
    cache = cache_controller()
    old_data = get_from_cache(cep)
    if old_data:
        cep = CEP_MODEL()
        cep.load_data(old_data)
        print("****")
        print("Cache hit")
        return cep
    data = cep_obj.get_cep_info(cep)
    cache.write_json(cep, data)
    cep = CEP_MODEL()
    cep.load_data(data)
    return cep


@blueprint.route('/api/register', methods=['POST'])
@log_request
@log_exception
@log_db_operation
def register():
    data: Dict = request.get_json() or {}
    nome: str = data.get("nome", "")
    email: str = data.get("email", "")
    cep: str = data.get("cep", "")
    if not nome or not email or not cep:
        return jsonify({"message": "Dados insuficientes", "required": ["nome", "email", "cep"]}), 400
    old_user: Optional[USER] = USER.query.filter_by(email=email).first()
    if old_user:
        return jsonify({"message": "Usuário já cadastrado"}), 400

    user: USER = USER(nome=nome, email=email)
    user.generate_hash()
    user.generate_apikey()
    db.session.add(user)
    cep_obj: CEP = CEP(usuario_id=user.user_hash)
    cep_info:CEP_MODEL = get_write_from_cache(cep, cep_obj)
    cep_obj.load_cep(cep_info)
    db.session.add(cep_obj)
    db.session.commit()
    return jsonify({"message": "Usuário registrado com sucesso", "apikey": user.apikey, "cep": cep_obj.as_dict()}), 201

@blueprint.route('/api/user_info', methods=['POST'])
@log_request
@log_exception
@log_db_operation
def user_info():
    data: Dict = request.get_json() or {}
    email: str = data.get("email", "")
    if not email:
        return jsonify({"message": "Email não informado"}), 400
    user: Optional[USER] = USER.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    return jsonify({"message": "Usuário encontrado", "user": user.as_dict()}), 200

@blueprint.route("/api/get_cep", methods=['GET'])
@verify_apikey
@log_request
@log_exception
@log_db_operation
def get_cep():
    data: Dict = request.args
    user: USER = g.user
    ceps: list[CEP] = g.ceps
    cep: str = data.get("cep", "")
    if not cep:
        return jsonify({"message": "CEP não informado"}), 400
    if cep in [c.cep for c in ceps]:
        return jsonify({"message": "CEP já registrado"}), 400
    cep_obj: CEP = CEP(usuario_id=user.user_hash)
    cep_info: CEP_MODEL = get_write_from_cache(cep, cep_obj)
    cep_obj.load_cep(cep_info)
    db.session.add(cep_obj)
    db.session.commit()
    return jsonify({"message": "CEP adicionado com sucesso", "cep": cep_obj.as_dict()}), 201

@blueprint.route("/api/get_ceps", methods=['GET'])
@verify_apikey
@log_request
@log_exception
@log_db_operation
def get_ceps():
    user: USER = g.user
    ceps: list[CEP] = g.ceps
    return jsonify({"user": user.as_dict(), "ceps": [cep.as_dict() for cep in ceps]}), 200

@blueprint.route("/api/change_data", methods=['POST'])
@verify_apikey
@log_request
@log_exception
@log_db_operation
def change_data():
    data: Dict = request.get_json() or {}
    user: USER = g.user
    ceps: list[CEP] = g.ceps
    old_cep: str = data.get("old_cep", "")
    cep_value: str = data.get("new_cep", "")

    if old_cep:
        old_cep = old_cep.replace("-", "")
        cep: Optional[CEP] = next((c for c in ceps if c.cep == old_cep), None)
        if not cep:
            return jsonify({"message": "CEP não encontrado"}), 404
        else:
            cep.cep = cep_value
            cep_info: CEP_MODEL = get_write_from_cache(cep_value, cep)
            cep.load_cep(cep_info)

    name: Optional[str] = data.get("nome")
    if name:
        user.nome = name
    email: Optional[str] = data.get("email")
    if email:
        user.email = email
    db.session.commit()
    return jsonify({"message": "Dados alterados com sucesso!", "user": user.as_dict(), "ceps": [cep.as_dict() for cep in ceps]}), 200

@blueprint.route("/api/delete_cep", methods=['POST'])
@verify_apikey
@log_request
@log_exception
@log_db_operation
def delete_cep():
    data: Dict = request.get_json() or {}
    user: USER = g.user
    ceps: list[CEP] = g.ceps
    cep: Optional[str] = data.get("cep")
    if not cep:
        return jsonify({"message": "CEP não informado"}), 400
    cep = cep.replace("-", "")
    cep_obj: Optional[CEP] = next((c for c in ceps if c.cep == cep), None)
    if not cep_obj:
        return jsonify({"message": "CEP não encontrado"}), 404
    db.session.delete(cep_obj)
    db.session.commit()
    return jsonify({"message": "CEP deletado com sucesso!"}), 200
