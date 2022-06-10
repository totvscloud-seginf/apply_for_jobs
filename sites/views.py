from traceback import print_tb
from urllib import response
from django.shortcuts import render,redirect
from django.middleware import csrf
import requests
from datetime import date,datetime

# Create your views here.
def index(rq):
    return render(rq,'index.html')

def get_password_id(rq,id):
    host = rq.META['HTTP_HOST']
    response = requests.get("http://{}/api/password/{}".format(host,id))
    json = response.json()

    # transforma o str da data gravado no banco em um valor date para 
    # a comparação
    str_date = json['expiration_date']
    obj_date = datetime.strptime(str_date,'%Y-%m-%d')
    expiration_date = obj_date.date()

    max_views = int(json['max_views'])
    views     = int(json['views']) 

    data = {
        'password': json['password'],
        'expiration_date': json['expiration_date'],
        'max_views': json['max_views'],
        'views': json['views'],
    }
        
    # valida se a senha pose ser mostrada 
    if max_views <= views or expiration_date < datetime.today().date():
        data['password'] = None
    else:
        views = views + 1
        data['views'] = views
        # atualiza o contador de visualizações

    
    response2 = requests.put("http://{}/api/password/{}".format(host,id),data)
    return render(rq,'detalhes_senha.html', data)

    #http://fantunesdev-password.herokuapp.com/passwords/504fce68-d616-4fb4-aadd-f9180adab1ee/

def create_password(rq):
    host = rq.META['HTTP_HOST']
    data = {
        'password': rq.POST["password"],
        'expiration_date': rq.POST["qt_dias"],
        'max_views': rq.POST["qt_visu"],
        'views': 0
    }
    response = requests.post("http://{}/api/password".format(host), data = data)
    json = response.json()
    return redirect('get_password_id', json['id'])
