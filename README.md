# AvaliaÃ§Ã£o de conhecimentos em Desenvolvimento de Software

## Considere os seguintes dados:
 
Url para acesso: https://main.d2shxk5imahqcz.amplifyapp.com
## Diagrama em anexo
Diagrama de processos.png
## Explicando o projeto
Primeiro eu fiz o front end, no começo tive uma certa dificuldade em rodas o ReactJS no AWS Amplify, mas no fim deu tudo certo, devido a imprevistos que eu acabei tendo durante a semana, acabei ficando alguns dias sem o computador deixando o prazo mais curto, por conta disso acabei fazendo um frontend mais simples, sem muita estética porém focando na sua funcionalidade.

Depois fui realizar o banco de dados utilizando o DynamoDB, fiz em MYSQL que é o que eu mais tenho prática, depois de tudo configurado consegui conectar tudo certo e partir para a função Lambda.

A função Lambda foi o mais divertido e desafiador de ser feito, primeiro precisava fazer uma função que pegava os dados do front end, criptografar a senha e incluía no banco de dados. Minha ideia inicial era fazer com Python já que seria a linguagem que eu mais tenho familiaridade, porém tive muita dificuldade de fazer o pyodbc funcionar no Lambda, nao sei se foi uma questão de configuração errada ou algo do tipo, no fim para não perder muito tempo optei por fazer via nodeJS mesmo. Pelo node utilizei o sequelize para fazer a integração com o banco de dados. Feito isso consegui inserir os dados, porém pensei em alterar um pouco a proposta. Utilize o nodemailer para enviar um email ao cliente com uma chave de acesso e com a mesma ele consegue visualizar a senha. Escolhi gerar e criptografar no backend por ser mais seguro e difícil de acessar caso alguém tenha intenções maliciosas. Somente a senha do email que envia a senha que está com baixa segurança, coloque em texto puro porém se tivesse um pouco mais tempo teria colocado em uma variável de ambiente.
Depois precisei fazer a função  para pegar os dados e fazer a lógica para verificar se o número de views ou as horas  já tinham expirado, e também apagar a senha caso o mesmo já tenha atingido o número de views ou o tempo apagando a senha.

Por fim, fui fazer o API Gateway, foi a parte mais simples do processo, fiz a API e fiz os métodos para chamar no front e conectar com a função Lambda.


## Segurança :
Primeiro que eu não me preocupei em fazer um sistemas de usuários,preferi focar apenas na parte de fazer o código funcionar.
O sistema se protege de alguns tipos de ataques, porém o mesmo apresenta algumas vulnerabilidades ( como por exemplo dados sensíveis em texto puro).
Considerando o OWASP 10 o programa se protege de alguns tipos de ataques com injection, já que não é possível injetar SQL por exemplo.
Insecurence design também é outro exemplo, em sistemas como C++ builder são sistemas inseguros.
Security Misconfiguration.
Componentes vulneráveis, só utilizei componentes que recebem atualização índice de seguranca.
São alguns exemplos do OWASP 10 que o sistema está nos conformes.
Ficou faltando os logs que eu gostaria de ter incluído mas infelizmente não consegui fazer a tempo, mas julgo muito importante para verificar se o sistema está sendo atacado e gerar uma auditoria do sistema.
Os logs são extremamente importantes, eu já implementei e utilizo até hoje nos sistemas em que eu trabalho, fazendo uma conexão com uma api do telegram e enviando todos os logs para meu celular assim monitorando os ataques, como eu disse antes infelizmente não deu tempo de implementar esse sistema