from pydantic import BaseModel
from typing import List

from model.hardware import Hardware



class HardwareSchema(BaseModel):
    """ Define como um novo hardware a ser inserido deve ser representado
    """
    tipo: str = "Placa de Video"
    marca: str = "Asus"
    modelo: str = "RTX 4090"
    valor: float = 12.899


class HardwareBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no tipo do hardware.
    """
    tipo: str = "Exemplo"


class ListarHardwaresSchema(BaseModel):
    """ Define como uma listagem de hardwares que será retornada.
    """
    hardwares:List[HardwareSchema]


def apresenta_hardwares(hardwares: List[Hardware]):
    """ Retorna uma representação do hardware seguindo o schema definido em
        HardwareViewSchema.
    """
    result = []
    for hardware in hardwares:
        result.append({
            "tipo": hardware.tipo,
            "marca": hardware.marca,
            "modelo": hardware.modelo,
            "valor": hardware.valor,
        })

    return {"hardwares": result}


class HardwareViewSchema(BaseModel):
    """ Define como um hardware será retornado.
    """
    id: int = 1
    tipo: str = "Placa de Video"
    marca: str = "Asus"
    modelo: str = "RTX 4090"
    valor: float = 12.899


class HardwareDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    tipo: str

def apresenta_hardware(hardware: Hardware):
    """ Retorna uma representação do hardware seguindo o schema definido em
        HardwareViewSchema.
    """
    return {
        "id": hardware.id,
        "tipo": hardware.tipo,
        "marca": hardware.marca,
        "modelo": hardware.modelo,
        "valor": hardware.valor
    }
