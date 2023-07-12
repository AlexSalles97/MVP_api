from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Importa os elementos definidos no modelo
from model.base import Base
from model.hardware import Hardware

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
    # Cria o diretorio
    os.makedirs(db_path)

# url de acesso ao banco de dados
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# cria a engine de conexão com o banco de dados
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco de dados
Session = sessionmaker(bind=engine)

# cria o banco de dados se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco de dados, caso não existam
Base.metadata.create_all(engine)