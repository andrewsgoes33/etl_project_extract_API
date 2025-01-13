import time
import requests
from tinydb import TinyDB
from datetime import datetime

#função para chamar a API e gravar retornando os dados no formato JSON
def extract_dados_bitcoin():
    url = 'https://api.coinbase.com/v2/prices/spot'
    response = requests.get(url)
    dados = response.json()
    return dados

#Função para acessar o segundo nível do JSON e trocar o nome das colunas armazenando em um novo JSON
def transform_dados_bitcoin(dados):
    valor = dados['data']['amount']
    criptomoeda = dados['data']['base']
    moeda = dados['data']['currency']
    timestamp = datetime.now().timestamp()
    dados_transformados = {
        'valor' : valor,
        'criptomoeda' : criptomoeda,
        'moeda' : moeda,
        'timestamp' : timestamp
    }
    
    return dados_transformados

#função para salvar no banco de dados
def salvar_dados_tinydb(dados, db_name='bitcoin.json'):
    db = TinyDB(db_name)
    db.insert(dados)
    print('Dados salvos com sucesso!')
    

if __name__ == "__main__":
    #Extração dos dados
    while True:
        dados_json = extract_dados_bitcoin()
        dados_tratados = transform_dados_bitcoin(dados_json)
        salvar_dados_tinydb(dados_tratados)
        time.sleep(15)


#Código printar o resultado da função, buscando a coluna 'amount' dentro da coluna 'data'
#print(extract_dados_bitcoin()['data']['amount'])