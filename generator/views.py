from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime

from generator.entities.password import Password
from generator.forms import password_form
from generator.forms.gerenal_form import ExclusionForm
from generator.repositories import password_repository, access_repository
from generator.services import password_service, access_service

# Create your views here.

template_tags = {
    'ano_atual': datetime.today().year
}


@login_required
def create_password(request):
    """
    Instancia um objeto do tipo PasswordForm passando-o para o template. Le os campos do template, cria uma instancia da
    classe Password e passa para o service fazer o cadastro no banco de dados.
    :param request: Instancia da requisicaoo HTTP
    :return: Se o verbo HTTP for GET, esta abrindo a página e renderiza o template de cadastro de senha. Seo verbo HTTP
    for POST, coleta os valores do formulario, insere-os numa instância da classe Password e passa para o service fazer
    o cadastro.
    """
    if request.method == 'POST':
        form_password = password_form.PasswordForm(request.POST)
        if form_password.is_valid():
            new_password = Password(
                value=form_password.cleaned_data['value'],
                expiration_date=form_password.cleaned_data['expiration_date'],
                maximum_views=form_password.cleaned_data['maximum_views'],
                views=0
            )
            password_db = password_service.create_password(new_password)
            return redirect('get_password_id', password_db.id)
    else:
        form_password = password_form.PasswordForm()
    template_tags['form_password'] = form_password
    return render(request, 'password/form_password.html', template_tags)


@login_required
def get_passwords(request):
    """
    Solicita ao service todos os passwords cadastrados e passa a variável para o template.
    :param request: Instancia da requisição HTTP
    :return: Renderiza o template que exibe todos os passwords gravados.
    """
    passwords = password_service.get_passwords()
    template_tags['passwords'] = passwords
    return render(request, 'password/get_passwords.html', template_tags)


def get_password_id(request, id):
    """
    Método que exibe o link com a senha para o usuario final. Solicita ao service a instancia do model Password que
    corresponde ao 'id' passado na URL. Passa ao repositório validar as regras de incrementacao do campo view.
    Registra a hora e o ip do acesso.
    :param request: Instancia da requisicao HTTP
    :param id: String do 'id' a ser buscado no banco de dados.
    :return: Renderiza o template e exibe a senha gerada para o usuario final.
    """
    if request.user.is_authenticated:
        password = password_service.get_password_id(id)
        access = access_service.get_access_password(password)
        template_tags['access'] = access
    else:
        password = password_repository.increment_view(id)
        access_repository.register_access(request, password)
    template_tags['password'] = password
    return render(request, 'password/password_details.html', template_tags)


@login_required
def delete_password(request, id):
    """
    Deleta um registro do Password e as informações de acesso a partir de um id.
    :param request: Instancia da requisicao HTTP
    :param id: String do 'id' a ser buscado no banco de dados.
    :return: Renderiza o template da página de confirmacao de exclusao.
    """
    password = password_service.get_password_id(id)
    if request.POST.get('confirmation'):
        password_service.delete_password(password)
        return redirect('get_passwords')
    template_tags['password'] = password
    template_tags['exclusion_form'] = ExclusionForm()
    return render(request, 'password/password_details.html', template_tags)


@login_required
def delete_expirated(request):
    """
    Deleta todos os registros de Password que expiraram, bem como as informações de acesso, como data/hora e ip.
    :param request: Instancia da requisicao HTTP
    :return: Renderiza o template da página de confirmacao de exclusao dos passwords.
    """
    passwords = password_service.get_expirated_passords()
    if request.POST.get('confirmation'):
        for password in passwords:
            password_service.delete_password(password)
        return redirect('get_passwords')
    template_tags['passwords'] = passwords
    template_tags['exclusion_form'] = ExclusionForm()
    return render(request, 'password/get_passwords.html', template_tags)


def login_user(request):
    """
    Cria uma sessao para o administrador
    :param request: Instancia da requisicao HTTP
    :return: Renderiza o template da pagina de login.
    """
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('create_password')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'login/login.html', {'form_login': form_login})


@login_required
def logout_user(request):
    """
    Encerra a sessao do administrador.
    :param request: Instancia da requisicao HTTP
    """
    logout(request)
    return redirect('login_user')
