from generator.models import Password


def create_password(password):
    """
    Registra uma instancia do tipo Password no banco de dados.
    :param password: Recebe uma instância do tipo password.
    :return: Retorna a instância cadastrada no banco.
    """
    password_db = Password.objects.create(
        value=password.value,
        expiration_date=password.expiration_date,
        maximum_views=password.maximum_views,
        views=password.views
    )
    return password_db


def get_passwords():
    """
    Obtem todos os cadastros registrados no banco de dados do model Password.
    :return: Retorna um QuerySet com uma lista de todas as instâncias do model Password.
    """
    return Password.objects.all()


def get_expirated_passords():
    """
    Obtem todos os cadastros do model Password que estão com o campo 'value' em branco porque expiraram.
    :return: Retorna um QuerySet com todos os registros do model Password.
    """
    return Password.objects.filter(value__isnull=True)


def get_password_id(id):
    """
    Obtem um registro do Model Password com a partir de um id.
    :param id: String com o 'id' a ser buscado no banco de dados.
    :return: Retorna uma instância do Model Password que corresponde ao 'id' buscado.
    """
    return Password.objects.get(id=id)


def edit_password(old_password, new_passowrd):
    """
    Edita um registro do model Password no banco de dados.
    :param old_password: Recebe o Model do tipo Password com os dados antigos.
    :param new_passowrd: Recebe uma instância da classe Password com os dados novos.
    :return: Retorna uma instãncia do objeto cadastrado no banco de dados.
    """
    old_password.value = new_passowrd.value
    old_password.expiration_date = new_passowrd.expiration_date
    old_password.maximum_views = new_passowrd.maximum_views
    old_password.views = new_passowrd.views
    old_password.save(force_update=True)
    return old_password


def delete_password(password):
    """
    Exclui um registro do model Password no banco de dados.
    :param password: Recebe uma instância do model Password.
    """
    password.delete()
