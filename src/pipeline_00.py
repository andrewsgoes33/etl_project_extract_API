import requests
from tinydb import TinyDB

url = 'https://api.coinbase.com/v2/prices/spot'


def extract_dados_bitcoin():
    response = requests.get(url)
    dados = response.json()
    return dados

def transform_dados_bitcoin(dados):
    valor = dados['data']['amount']
    criptomoeda = dados['data']['base']
    moeda = dados['data']['currency']
    
    dados_transformados = {
        'valor':valor,
        'criptomoeda':criptomoeda,
        'moeda':moeda
    }
    
    return dados_transformados

def salvar_dados_tinydb(dados, db_name='bitcoin.json'):
    db = TinyDB(df_name)
    

if __name__ == '__main__':
    #Extração dos dados
    dados_json = extract_dados_bitcoin()
    dados_tratados = transform_dados_bitcoin(dados_json)
    print(dados_tratados)