# Avaliação de conhecimentos em Desenvolvimento de Software

## Considerações sobre o projeto Philipe Couto:
 
Esse é meu projeto concluido do desafio da Totvs.
### Diagrama
![Aqui está o diagrama do projeto](./Totvs-PassRec.drawio.svg) 



## Explicações



Para o backend eu escolhi utilizar python por estar mais familizarizado com a lingaugem.

A estrutura conta com a pasta AWS que contem as classes utilizadas dento do AWS lambda para resolução.

Dentro da estruta estão contidos:
 - request.py* - que é a função main do AWS Lambda, aqui o há os endpoints de para cada uma das requisições que são realizadas pelo front-end, passando pelo API Gateway onde há um proxy que recebe a variação dos links

 *Por falta de prática com o AWS não consegui resolver de outra forma, além de não conseguir criar o mecanismo para resolver o erro de CORS

 - user.py - Nesse arquivo está a classe user que resolve todos os pontos do desafio é apartir dessa classe que os dados são validados pelo backend e retornados ao front-end e é dentro dessa classe que é realizada a chamada no arquivo passGenerator.py que contem a classe passGen.

- passGenerator.py - Nesse arquivo está contida a classe passGen

- conn.py - Nesse arquivo está a classe Database que realiza as operações dentro do DynamoDB, aqui o sistema valida as requisições do ponto de vista de banco de dados, como validar existencia de senha repetida, se existe ou não usuário e retorna caso tudo esteja correto.

 - ### PASSGEN
   - É aqui que é resolvido a geração automática de password e a codificação do password antes de enviar para o banco de dados

- ### VALIDAÇÕES
   - Na classe user.py há validações que verificam se o password já expirou ou se há visualizações disponíveis, para resolver questões gerais de tempo eu defini que as datas devem ser convertidas em epoch
   - Caso a senha já tenha sido expirada ou não tenha mais visualizações liberadas, ela <strong>não</strong> removida da base, eu optei por isso para poder evitar que o usuário preencha uma senha repetida e isso poderia causar problemas de integridade dos dados, por esse motivo eu decidi marcar o password como inativo.
   - As validações de tempo e visualização são executadas paralelamente, assim caso uma das condições não esteja válida o sistema retorna que a senha expirou.

## Demostração das requisições e respostas
 Aqui eu decidi colocar um exemplo da estrutura json de requisição

``` 
json = {login: '',
            password: {
                        password: '',
                        auto: '',
                        passlimitview: '',
                        passlifetime: '',
                        currentlink: '',
                        params: {
                                passlen: '',
                                numbers: '',
                                letter: '',
                                espChar: ''
                        }
                    }
        }
```

### Demonstração da estrutura do banco de dados DynamoDB
 - tabela users:
    ```
       _user = {
                'userid': int(value),
                'login' : str(user)
            }
    ```
 - tabela userpass:
   ```
       userpass_item = {
                'passid': int(value),
                'userid': userid,
                'password': str(decoded(pass))
                'passlifetime': int(passlifetime),
                'passlimitview': int(passlimitview),
                'currentlink': str(currentlink),
                'passtatus' : 1
            }
   ```


# Considerações

Nesse projeto eu compreendi que o usuário pode ou não ser uma pessoa que usa o login, de qualquer forma eu defini que para <strong>TODOS</strong> deve sempre haver um login. Pensando em um sistema não fazia muito sentido para mim recuperar senha sem que tivesse um login.

Considerei que todas as senhas poderiam ser informação relevante, porntando julguei prudente sempre mante-las no banco de dados, assim evitando que o usuário repita a senha que ao meu ver tenta mitigar problema com senha roubada.

--O projeto não sofreu build--

# Execução
 
``` 
npm start run
```


