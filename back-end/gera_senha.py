import boto3
import json 

#importa o módulo random do python
from random import choice

#importa o módulo string
import string

#importa data
from datetime import datetime, timedelta

#importa o modulo de hash para a url dinamica
import hashlib
from os import urandom


def lambda_handler(event, context):
	
	complexidade = ''

	#valida os valores enviados
	for k in event.keys():	
		if type(event[k]) != int or event[k] < 0:
			return {
			'statusCode': 400,
			'body': json.dumps({"mensagem": "Erro ao processar as informações"})
			}
		else:
			if k == "tamanho":
				if event[k] > 64:
					return {
						'statusCode': 400,
						'body': json.dumps({"mensagem": "Tamanho fornecido para a senha é inválido"})
					}
			elif k == "letter" and event[k] == 1:
				complexidade = complexidade + string.ascii_letters
			elif k == "nums" and event[k] == 1:
				complexidade = complexidade + string.digits
			elif k == "special" and event[k] == 1:
				complexidade = complexidade + string.punctuation
			elif k == "views" and event[k] > 100 or k == "views" and event[k] == 0:
				return {
					'statusCode': 400,
					'body': json.dumps({"mensagem": "Em 'Visualizações Máximas' escolha um valor entre 1 e 100"})
				}
			elif k == "valida" and event[k] > 90 or k == "valida" and event[k] == 0:
				return {
					'statusCode': 400,
					'body': json.dumps({"mensagem": "Em 'Validade (em Dias)' escolha um valor entre 1 e 90"})
				}
			
	#confirma se foi escolhido ao menos uma opção para o formato da senha
	if complexidade == '':
		return {
			'statusCode': 400,
			'body': json.dumps({"mensagem": "Escolha ao menos uma das opções de formato para a senha."})
		}
		
	#chama o BD
	dynamodb = boto3.resource('dynamodb')
	tabela = dynamodb.Table('SenhaCliente') #altere 'SenhaCliente' pelo nome da tabela

	#consulta o BD para ver se alguma senha já foi gerada
	#item = []
	resposta_consulta = tabela.get_item(Key={'id': 1})
	
	if 'Item' not in resposta_consulta:
		senha_gerada = gerar_senha(event, complexidade)
		
		#grava senha no bd
		try:
		    tabela.put_item(
    			Item = {
    				'id': 1,
    				'senha': senha_gerada["senha"],
    				'views_m': senha_gerada["views_m"],
    				'views': 0,
    				'validade': senha_gerada["validade"],
    				'parametro': senha_gerada["parametro"]
    			}
    		)
		except Exception as e:
			return {
				'statusCode': 500,
				'body': json.dumps({"mensagem": "Erro ao gravar a senha."})
			}
		
		return {
			'statusCode': 200,
			'body': json.dumps(senha_gerada)
		}
		
				
	else:
		#se já tiver uma senha gerada, verifica se ela está ativa
		if resposta_consulta['Item']['views'] >= resposta_consulta['Item']['views_m'] or resposta_consulta['Item']['validade'] < str(datetime.now()):
			#se não estiver ativa, deleta e gera uma nova e grava no bd
			tabela.delete_item(
				Key={'id': 1}
			)
			senha_gerada = gerar_senha(event, complexidade)

			try:
			    resposta = tabela.put_item(
				Item = {
					'id': 1,
					'senha': senha_gerada["senha"],
					'views_m': senha_gerada["views_m"],
					'views': 0,
					'validade': senha_gerada["validade"],
					'parametro': senha_gerada["parametro"]
				}
			)
			except Exception as e:
				return {
					'statusCode': 500,
					'body': json.dumps({"mensagem": "Erro ao gravar a senha."})
				}
			
			return {
				'statusCode': 200,
				'body': json.dumps(senha_gerada)
			}
		else:
			#caso a senha ainda esteja válida, informa que já tem uma senha válida criada
			return {
			'statusCode': 400,
			'body': json.dumps({"mensagem": "Já existe uma senha criada."})
			}


#função que cria a senha conforme a complexidade passada
def gerar_senha(event, complexidade): 

	senha = ''
	nova_senha = {}
	views = event["views"]
	validade = str(datetime.now() + timedelta(days = event["valida"]))
	url_hash = hashlib.sha256(urandom(8)).hexdigest()[:34]
	
	for i in range(event["tamanho"]):
		senha += choice(complexidade)

	nova_senha["senha"] = senha
	nova_senha["views_m"] = views
	nova_senha["validade"] = validade
	nova_senha["parametro"] = url_hash

	return nova_senha
	