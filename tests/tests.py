import requests
from dotenv import load_dotenv
import os
load_dotenv()
basepoint = os.getenv("BACKEND_URL")
def test_user_registration():
    url = basepoint + "/api/register"
    data = {
    "nome":"lucas2",
    "email":"asuma3122@gmail.com",
    "cep":"86055-653"
}
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Usuário cadastrado com sucesso!")
        print(response.json())
    else:
        print(f"Falha ao cadastrar usuário. Status Code: {response.status_code}")
        print(response.text)

def test_get_new_cep():
    url = basepoint + "/api/get_cep"
    headers = {
        "apikey": "bbb8e11641aa55eaa442884669eb0c8820cfaed4e7d2b626299c7b2730c18d25"
    }
    args = {
        "cep": "86010350"
    }
    response = requests.get(url, params=args, headers=headers)
    if response.status_code == 201:
        print("CEP obtido com sucesso!")
        print(response.json())
    else:
        print(f"Falha ao obter CEP. Status Code: {response.status_code}")
        print(response.text)

def test_get_user_info():
    url = basepoint + "/api/user_info"
    data = {
        "email": "asuma3122@gmail.com"
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Informações do usuário obtidas com sucesso:")
        print(response.json())
    else:
        print(f"Falha ao obter informações do usuário. Status Code: {response.status_code}")


def test_get_all_ceps():
    url = basepoint + "/api/get_ceps"
    headers = {
        "apikey": "23ebc684e7819ee5c9ecae62e34a50b82d1564697aa2f84a9790bd6aa6669ab4"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("CEPs obtidos com sucesso:")
        print(response.json())
    else:
        print(f"Falha ao obter CEPs. Status Code: {response.status_code}")
        print(response.text)

def test_change_data():
    url = basepoint + "/api/change_data"
    data = {
        "old_cep": "86055-653",
        "new_cep": "86010-350",
    }
    headers = {
        "apikey": "23ebc684e7819ee5c9ecae62e34a50b82d1564697aa2f84a9790bd6aa6669ab4"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("CEP alterado com sucesso!")
        print(response.json())
    else:
        print(f"Falha ao alterar CEP. Status Code: {response.status_code}")
        print(response.text)

def test_delete_cep():
    url = basepoint + "/api/delete_cep"
    data = {
        "cep": "86010-350"
    }
    headers = {
        "apikey": "23ebc684e7819ee5c9ecae62e34a50b82d1564697aa2f84a9790bd6aa6669ab4"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("CEP deletado com sucesso!")
        print(response.json())
    else:
        print(f"Falha ao deletar CEP. Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_get_user_info()
    test_get_new_cep()