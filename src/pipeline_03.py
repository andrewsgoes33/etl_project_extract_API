import time
import requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from database import Base, BitcoinPreco

# Carrega variáveis de ambiente do arquivo.env
load_dotenv()

# Lê as variáveis separadas do arquivo .env (sem SSL)
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

#Constrói a URL de conexão com o banco de dados
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
)

#Cria o engine e a sessão
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def criar_tabela():
    """Cria a tabela no banco de dados, se não existir."""
    Base.metadata.create_all(engine)
    print("Tabela criada/verificada com sucesso!")
    
    
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
    timestamp = datetime.now()
    dados_transformados = {
        'valor' : valor,
        'criptomoeda' : criptomoeda,
        'moeda' : moeda,
        'timestamp' : timestamp
    }
    
    return dados_transformados

#função para salvar no banco de dados
def salvar_dados_postgres(dados):
    """Salva os dados no banco PostgreSQL."""
    session = Session()
    novo_registro = BitcoinPreco(**dados)
    session.add(novo_registro)
    session.commit()
    session.close()
    print(f"[{dados['timestamp']}] Dados salvos no PostgreSQL!")
    

if __name__ == "__main__":
    criar_tabela()
    print('Iniciando ETL com atualização a cada 15 segundos... (CRTL+C para interromper)')
    
    #Extração dos dados
    while True:
        try:
            dados_json = extract_dados_bitcoin()
            if dados_json:
                dados_tratados = transform_dados_bitcoin(dados_json)
                print('Dados Tratados:', dados_tratados)
                salvar_dados_postgres(dados_tratados)
            time.sleep(15)
            
        except KeyboardInterrupt:
            print('\nProcesso interrompido pelo usuário. Finalizando...')
            break
        except Exception as e:
            print(f'Erro durante a execução: {e})')
            time.sleep(15)
        
