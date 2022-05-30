from datetime import datetime

from generator.entities.password import Password
from generator.services import password_service


def increment_view(id):
    """
    Incrementa a visulização ou apaga o registro do valor do objeto do tipo Password caso o número máximo de
    visualizacoes ja tenha sido atingido.
    :param id: String com o id da instância Password.
    :return: Password cadastrado no banco de dados.
    """
    old_password = password_service.get_password_id(id)
    new_password = Password(
        value=old_password.value,
        expiration_date=old_password.expiration_date,
        maximum_views=old_password.maximum_views,
        views=old_password.views
    )
    if old_password.views >= old_password.maximum_views or old_password.expiration_date < datetime.today().date():
        new_password.value = None
    else:
        new_password.views += 1
    return password_service.edit_password(old_password, new_password)
