from dataclasses import dataclass

@dataclass
class CEP_MODEL:
    cep: str = None
    logradouro: str = None
    complemento: str = None
    bairro: str = None
    localidade: str = None
    uf: str = None
    estado: str = None
    regiao: str = None
    ibge: str = None
    gia: str = None
    ddd: str = None
    siafi: str = None

    def load_data(self, data: dict) -> None:
        self.cep = data.get('cep')
        self.logradouro = data.get('logradouro')
        self.complemento = data.get('complemento')
        self.bairro = data.get('bairro')
        self.localidade = data.get('localidade')
        self.uf = data.get('uf')
        self.estado = data.get('estado')
        self.regiao = data.get('regiao')
        self.ibge = data.get('ibge')
        self.gia = data.get('gia')
        self.ddd = data.get('ddd')
        self.siafi = data.get('siafi')
