from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String
from typing import Union

from  model import Base

class Hardware(Base):
    __tablename__ = 'hardware'

    id = Column("pk_hardware", Integer, primary_key=True)
    tipo = Column(String(100), unique=True)
    marca = Column(String(100))
    modelo = Column(String(100))
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, tipo:str, marca:str, modelo:str, valor:float, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria a tabela Hardware

        Arguments:
            tipo: tipo de hardware
            marca: marca do hardware
            modelo: modelo do hardware
            valor: valor esperado para o hardware
            data_insercao: data de quando o hardware foi inserido à base
        """
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo
        self.valor = valor

        # se não for informada, será o data exata da inserção no banco de dados
        if data_insercao:
            self.data_insercao = data_insercao