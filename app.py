from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote

from model import Session, Hardware
from schemas import *

info = Info(title="Api Vendas", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definição de tags
home_tag = Tag(name="Documentação", description="Seleção de Documentação: Swagger, Redoc ou RapiDoc")
hardware_tag = Tag(name="Hardware", description="Adição, visualização e remoção de hardwares à base")

@app.get('/', tags=[home_tag])
def home():
    """Faz o redirecionamento para /openapi, tela onde permite a escolha de documentação.
    """
    return redirect('/openapi')

@app.post('/hardware', tags=[hardware_tag],
          responses={"200": HardwareViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_hardware(form: HardwareSchema):
    """Realiza a adição de um novo hardware à base de dados.
    
    Faz o retorno de uma representação dos hardwares.
    """
    hardware = Hardware(
        tipo=form.tipo,
        marca=form.marca,
        modelo=form.modelo,
        valor=form.valor)

    try:
        # Realiza a conexão com a base.
        session = Session()
        # Adiciona o hardware.
        session.add(hardware)
        # Efetiva o comando de adição da nova peça na tabela.
        session.commit()
        return apresenta_hardware(hardware), 200
 
    except IntegrityError as e:
        # A duplicidade do tipo é o motivo do IntegrityError.
        error_msg = "Hardware de mesmo nome já salvo na base :/"
        return {"message": error_msg}, 409

    except Exception as e:
        # Erro imprevisivel.
        error_msg = "Não foi possível salvar novo item :/"
        return {"message": error_msg}, 400

@app.get('/hardwares', tags=[hardware_tag],
         responses={"200": ListarHardwaresSchema, "404": ErrorSchema})
def get_hardwares():
    """Realiza a busca por todos os hardwares cadastrados.
    
    Faz o retorno da listagem de hardwares.
    """
    # Realiza a conexão com a base.
    session = Session()
    # Faz a busca.
    hardwares = session.query(Hardware).all()

    if not hardwares:
        # Se não há hardwares cadastrados.
        return {"hardwares": []}, 200
    else:
        # Retorna a representação do hardware.
        print(hardwares)
        return apresenta_hardwares(hardwares), 200
 
@app.get('/hardware', tags=[hardware_tag],
         responses={"200": HardwareViewSchema, "404": ErrorSchema})
def get_hardware(query: HardwareBuscaSchema):
    """Realiza a busca por um hardware a partir do tipo do hardware.
    
    Faz o retorno de uma representação dos hardwares.
    """
    hardware_tipo = query.tipo
    # Realiza a conexão com a base.
    session = Session()
    # Faz a busca.
    hardware = session.query(Hardware).filter(Hardware.tipo == hardware_tipo).first()

    if not hardware:
        # Quando o hardware não é encontrado.
        error_msg = "Hardware não encontrado na base :/"
        return {"message": error_msg}, 404
    else:
        # Retorna a representação do hardware.
        return apresenta_hardware(hardware), 200

@app.delete('/hardware', tags=[hardware_tag],
            responses={"200": HardwareDelSchema, "404": ErrorSchema})
def del_hardware(query: HardwareBuscaSchema):
    """Realiza a exclusão de um hardware a partir do tipo de hardware informado.
    
    Faz o retorno de uma mensagem de confirmação de exclusão.
    """
    hardware_tipo = unquote(unquote(query.tipo))
    print(hardware_tipo)
    # Realiza a conexão com a base.
    session = Session()
    # Exclui o hardware.
    count = session.query(Hardware).filter(Hardware.tipo == hardware_tipo).delete()
    session.commit()
    if count:
        # Retorna a representação da mensagem de confirmação.
        return {"message": "Hardware removido", "id": hardware_tipo}
    else:
        # Quando o hardware não é encontrado.
        error_msg = "Hardware não encontrado na base :/"
        return {"message": error_msg}, 404
