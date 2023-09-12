import boto3
import json 

#importa data
from datetime import datetime, timedelta

def lambda_handler(event, context):

	#valida o valor enviado
	if (len(event["parametro"]) != 34):
		return {
			'statusCode': 400,
			'body': json.dumps(0)
		}
	else:
		#chama o BD
		dynamodb = boto3.resource('dynamodb')
		tabela = dynamodb.Table('SenhaCliente') #altere 'SenhaCliente' pelo nome da tabela

		#consulta o BD
		resposta_consulta = tabela.get_item(Key={'id': 1})

		#verifica se tem algum item no BD
		if 'Item' not in resposta_consulta:
			return {
			'statusCode': 400,
			'body': json.dumps(0)
			}
		else:
			#verifica se o parametro da URL é válido
			if resposta_consulta['Item']['parametro'] != event["parametro"]:
				return {
				'statusCode': 400,
				'body': json.dumps(0)
				}
			else:
				#adiciona +1 ao contador de visualizações
				visualizacoes = resposta_consulta['Item']['views'] + 1

				#verifica se o número de visualizações máximas ou a validade da senha excedeu
				if visualizacoes > resposta_consulta['Item']['views_m'] or resposta_consulta['Item']['validade'] < str(datetime.now()):
					
					#se excedeu o limite, deleta a senha do BD
					tabela.delete_item(
						Key={'id': 1}
					)
					return {
					'statusCode': 400,
					'body': json.dumps(0)
					}
				else:
					try:
						#caso a senha esteja disponível, atualiza o contador de visualizações com +1
						tabela.update_item(
							Key={
							'id': 1
							},
							UpdateExpression='SET #v = :novo_valor',
						        ExpressionAttributeNames={
						            '#v': 'views'
						    },
							ExpressionAttributeValues={
								':novo_valor': visualizacoes
							}
						)
					except Exception as e:
						return {
							'statusCode': 500,
							'body': json.dumps(0)
						}
					
					#retorna com o valor da senha
					return {
						'statusCode': 200,
						'body': json.dumps({"senha": resposta_consulta['Item']['senha']})
					}
