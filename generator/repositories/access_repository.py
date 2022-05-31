from datetime import datetime

from ipware import get_client_ip

from generator.entities.access import Access
from generator.services import access_service


def register_access(request, password):
    """
    Instancia um objeto do tipo Access e chama o método responsável pelo registro no banco de dados.
    :param request: Requisição HTTP.
    :param password: Objeto do tipo Password, necessario para fazer o vinculo entre o acesso e o password.
    :return: Retorna o objeto cadastrado no Banco de Dados.
    """
    access = Access(
        password=password,
        date=datetime.now(),
        ip=get_client_ip(request)[0]
    )
    return access_service.create_access(access)
