from generator.models import Access


def create_access(access):
    """
    Registra a intancia do tipo Access no banco de dados.
    :param access: Instancia da classe Access.
    :return: Retorna a instancia cadastrada no banco de dados.
    """
    access_db = Access.objects.create(
        password=access.password,
        date=access.date,
        ip=access.ip
    )
    return access_db


def get_access():
    """
    Busca todos os registros cadastrados no model Access.
    :return: Retorna um objeto do tipo QuerySet que eh uma lista de todos os cadastros do model Access.
    """
    return Access.objects.all()


def get_access_password(password):
    """
    Retorna todos os cadastros do model Access que possuem vinculo com o password.
    :param password: Instancia do tipo Password
    :return: Retorna um objeto do tipo QuerySet que eh uma lista com todos os cadastros do model Access e que possuem
    vinculo com o model Password.
    """
    return Access.objects.select_related('password').filter(password=password)
