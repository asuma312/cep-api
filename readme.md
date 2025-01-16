# Guia de Uso

## Pré-requisitos

- **Python versão 3.12**

### Instalação de Dependências

Para instalar as dependências necessárias, execute o comando:
```bash
pip install -r requirements.txt
```

---

## Configuração

1. **Caminho do Banco de Dados**
   - Edite o arquivo `.env` e altere o caminho da variável `DB_PATH` para apontar para sua pasta `static/db`.

2. **Configuração da Porta**
   - Caso altere a porta do aplicativo, atualize também a variável correspondente no arquivo `.env` para garantir que os testes funcionem corretamente.

---

## Exemplos de Uso

### 1. Registro de Usuário
#### Endpoint
`POST /api/register`

#### Exemplo de Requisição:
```python
import requests

url = "<BACKEND_URL>/api/register"
data = {
    "nome": "lucas2",
    "email": "asuma3122@gmail.com",
    "cep": "86055-653"
}
response = requests.post(url, json=data)

if response.status_code == 201:
    print("Usuário cadastrado com sucesso!")
    print(response.json())
else:
    print(f"Falha ao cadastrar usuário. Status Code: {response.status_code}")
    print(response.text)
```

---

### 2. Obter CEP
#### Endpoint
`GET /api/get_cep`

#### Exemplo de Requisição:
```python
import requests

url = "<BACKEND_URL>/api/get_cep"
headers = {
    "apikey": "<API_KEY>"
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
```

---

### 3. Informações do Usuário
#### Endpoint
`POST /api/user_info`

#### Exemplo de Requisição:
```python
import requests

url = "<BACKEND_URL>/api/user_info"
data = {
    "email": "asuma3122@gmail.com"
}
response = requests.post(url, json=data)

if response.status_code == 200:
    print("Informações do usuário obtidas com sucesso:")
    print(response.json())
else:
    print(f"Falha ao obter informações do usuário. Status Code: {response.status_code}")
```

---

### 4. Obter Todos os CEPs
#### Endpoint
`GET /api/get_ceps`

#### Exemplo de Requisição:
```python
import requests

url = "<BACKEND_URL>/api/get_ceps"
headers = {
    "apikey": "<API_KEY>"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("CEPs obtidos com sucesso:")
    print(response.json())
else:
    print(f"Falha ao obter CEPs. Status Code: {response.status_code}")
    print(response.text)
```

---

### 5. Alterar Dados
#### Endpoint
`POST /api/change_data`

#### Exemplo de Requisição:
```python
import requests

url = "<BACKEND_URL>/api/change_data"
data = {
    "old_cep": "86055-653",
    "new_cep": "86010-350",
}
headers = {
    "apikey": "<API_KEY>"
}
response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("CEP alterado com sucesso!")
    print(response.json())
else:
    print(f"Falha ao alterar CEP. Status Code: {response.status_code}")
    print(response.text)
```

---

### 6. Deletar CEP
#### Endpoint
`POST /api/delete_cep`

#### Exemplo de Requisição:
```python
import requests

url = "<BACKEND_URL>/api/delete_cep"
data = {
    "cep": "86010-350"
}
headers = {
    "apikey": "<API_KEY>"
}
response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("CEP deletado com sucesso!")
    print(response.json())
else:
    print(f"Falha ao deletar CEP. Status Code: {response.status_code}")
    print(response.text)
```

---

Agora o ambiente está pronto para uso! 🚀

