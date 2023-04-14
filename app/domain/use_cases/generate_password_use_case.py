
"""
Precisamos enviar uma senha de maneira segura para um cliente. Para isso, ao invés de encaminhá-la via E-mail, SMS, Slack, etc, foi dado como solução o desenvolvimento de um sistema com as seguintes funções:

1- Usuário irá inserir uma senha ou solicitar ao Sistema para gerar senha aleatória baseada em políticas de complexidade (tipo de caracteres, números, letras, tamanho, etc);

Exemplo1: o usuário digita sua senha no campo de texto;
Exemplo2: o usuário seleciona os parametros de complexidade de senha e ao clicar no botão "Gerar Senha" irá obter uma senha aleatória;
2- Usuário irá especificar quantas vezes a senha gerada poderá ser vista e qual o tempo que a senha ficará válida;

Exemplo: o usuário irá especificar que a senha possa ser vista apenas duas vezes pelo prazo de um dia;
3- O sistema irá gerar uma URL que dá acesso a visualização da senha, baseando-se nos critérios do item 02;

Exemplo: o usuário enviará a URL para que o cliente possa visualizar a senha;
4- Após atingir a quantidade de visualizações ou o tempo disponível, o sistema bloqueia/elimina a visualização da senha (expirado). A senha não deve ser armazenada após sua expiração

Exemplo1: Senha foi gerada para 2 visualizações e 2 dias de prazo. Cliente clicou na url 3 vezes seguidas no primeiro dia. 1º acesso: senha disponível e pôde ser visualizada. Contador atualizado para 1 view 2º acesso: senha disponível e pôde ser visualizada. Contador atualizado para 2 views=limite definido. Senha deletada 3º acesso: senha já deletada da base. Retorna mensagem de senha indispovível
Exemplo2: Senha foi gerada para 2 visualizações e 2 dias de prazo. Cliente só clicou na url depois de 4 dias que a mesma foi gerada. 1º acesso: senha já deletada da base após o prazo de 2 dias. Retorna mensagem de senha indispovível
Exemplo3: Senha foi gerada para 2 visualizações e 2 dias de prazo. Cliente clicou na url 2 vezes: uma assim que recebeu a mesma e a segunda depois de 5 dias. 1º acesso: senha disponível e pôde ser visualizada. Contador atualizado para 1 view 2º acesso: senha já deletada da base após o prazo de 2 dias. Retorna mensagem de senha indispovível
"""

import random
import datetime
from repositories.password_repository import PasswordRepository
from exceptions.invalid_visualizations_limit_error import InvalidVisualizationsLimitError
from exceptions.expired_password_error import ExpiredPasswordError
from entities.password import Password

class GeneratePasswordUseCase:
    def __init__(self, password_repository: PasswordRepository) -> None:
        self.password_repository = password_repository

    def execute(self, password: str, visualizations_limit: int, valid_until: datetime) -> Password:
        if visualizations_limit <= 0:
            raise InvalidVisualizationsLimitError

        password = Password(password, visualizations_limit, valid_until)
        self.password_repository.save_password(password)
        return password

    def generate_random_password(self, password_length: int, password_characters: str) -> str:
        password = ''.join(random.choice(password_characters) for i in range(password_length))
        return password

    def get_password_url(self, password: Password) -> str:
        url = self.password_repository.get_url_by_password(password)
        return url

    def retrieve_password(self, url: str) -> Password:
        password = self.password_repository.get_password_by_url(url)
        if password is None:
            raise PasswordNotFound
        return password

    def validate_password(self, password: str) -> bool:
        return self.password_repository.validate_password(password)

    def view_password(self, password: Password) -> str:
        if password.views_count >= password.visualizations_limit:
            raise InvalidVisualizationsLimitError
        if password.valid_until < datetime.now():
            raise ExpiredPasswordError

        password.views_count += 1
        return password.password

    def is_password_valid(self, password: Password) -> bool:
        return password.valid_until >= datetime.now() and password.views_count < password.visualizations_limit
    
    def delete_password(self, password: Password) -> None:
        self.password_repository.delete_password(password)
