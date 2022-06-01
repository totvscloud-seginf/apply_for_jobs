# Avaliação de conhecimentos em Desenvolvimento de Software

## Descrição da atividade:

Tecnologias utilizadas: React native, AWS(arquivo arquitetura.png): API Gateway, Lambda, IAM, DynamoDB.

Para a interface com usuário foi desenvolvido um frontend com react native contendo três campos: um para a quantidade de acessos no link que será gerado, outro para identificação do cliente e um para receber o link da senha.

Ao clicar no botão "Gerar senha" no frontend é chamado uma rota no API Gateway que se comunica com uma função Lambda e cria uma nova senha salvando no DynamoDB. O Lambda retorna uma url que é uma outra rota para ser enviada ao cliente onde conseguirá ver sua senha.
A rota enviada é um GET passando o id ( identificação do cliente mencionado acima) retornando sua senha e validando a quantidade de acessos que será feito através do link, basedo no parâmetro que foi passado (campo quantidade de acesso).


## Melhorias

1 - Adicionar um campo de tempo para expiração da senha.
2 - Gerar um link alternativo para o cliente para não haver altos custos de solicitações através da API.
