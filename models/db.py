from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
from datetime import datetime
from models.data_models import CEP_MODEL
import requests
import re
db = SQLAlchemy()
class USER(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.Boolean, nullable=False, default=True)
    apikey = db.Column(db.String(80), nullable=False)
    user_hash = db.Column(db.String(80), nullable=False)

    def generate_apikey(self):
        self.apikey = sha256(str(datetime.now()).encode()).hexdigest()
        return self.apikey

    def generate_hash(self):
        self.user_hash = f"{self.nome}-{self.email}"
        self.user_hash = sha256(self.user_hash.encode()).hexdigest()
        return self.user_hash

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class CEP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.String(80), db.ForeignKey('user.user_hash'), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    logradouro = db.Column(db.String(80), nullable=False)
    bairro = db.Column(db.String(80), nullable=False)
    cidade = db.Column(db.String(80), nullable=False)
    estado = db.Column(db.String(80), nullable=False)

    def get_cep_info(self, cep):
        cep = re.sub(r"\D", "", cep)
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        print(cep)
        if response.status_code != 200:
            raise Exception("Erro ao buscar CEP")
        data = response.json()
        data['cep'] = data['cep'].replace("-", "")
        return data

    def load_cep(self, data:CEP_MODEL):
        self.cep = data.cep
        self.logradouro = data.logradouro
        self.bairro = data.bairro
        self.cidade = data.localidade
        self.estado = data.uf

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
