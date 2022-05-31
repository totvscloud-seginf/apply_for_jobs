# Sistema para gerar senhas randômicas

O aplicativo pode ser acessado e testado com os dados abaixo: 
- **Link**: https://fantunesdev-password.herokuapp.com/
- **Login**: testes
- **Senha**: adminsite1


## Requisitos do projeto:
 
Precisamos enviar uma senha de maneira segura para um cliente. Para isso, ao invés de encaminhá-la via E-mail, SMS, Slack, etc, foi dado como solução o desenvolvimento de um sistema com as seguintes funções:
 
1- Sistema gera <strong>senha aleatória</strong> baseada em <strong>políticas de complexidade</strong> (tipo de caracteres, números, letras, tamanho, etc); 
- **Exemplo**: o usuário ao clicar no botão "Gerar Senha" irá obter uma senha aleatória;

2- Usuário irá especificar <strong>quantas vezes</strong> a senha gerada poderá ser vista e <strong>qual o tempo</strong> que a senha ficará válida;
- **Exemplo**: o usuário irá especificar que a senha possa ser vista apenas <em>duas vezes</em> pelo prazo de <em>um dia</em>;

3- O sistema irá <strong>gerar uma URL</strong> que dá acesso a visualização da senha, baseando-se nos critérios do item 02;
- **Exemplo**: o usuário enviará a URL para que o cliente possa visualizar a senha;

4- Após atingir a quantidade de visualizações ou o tempo disponível, o sistema <strong>bloqueia/elimina</strong> a visualização da senha (expirado).
A senha <strong>não deve ser armazenada</strong> após sua expiração

## Design

![alt text](https://uploaddeimagens.com.br/images/003/886/232/original/Tree.png?1653882054)


- A aplicação está dividida em duas partes, que segundo a documentação do Django são chamadas de apps. O app **generator** e o app **api**.
- O app **generator** serve o site.
- O app **api** serve as requisições http que são feitas pelo JavaScript ao back-end.
- De forma geral a aplicação está dividida em camadas. Além do sitema MTV habitual do Django, fizemos ainda algumas divisões para repartir responsabilidades que normalmente ficariam na **view**. Essa mudança tem vistas na melhoria da manutenibilidade do código. Permitindo que várias funcionalidades do código sejam corrigidas ou implementadas separadamente e deixando a camada **view** com a única responsabilidade chamar todas as variáveis necessárias para renderizar os templates. 
  1) A camada **entities** contém as classes utilizadas na aplicação.
  2) A camada **forms** é responsável pela criação e validação dos formulários renderizados no front-end.
  3) A camada **serializers**, presente apenas no app **api**, tem a mesma funcionalidade da camada **forms**, com a diferença de que as validações dos campos são feitas com base nas requisições solicitadas à API e não à renderização de formulários HTML.
  4) A camada **repositories** implemeta as regras de negócio da aplicação.
  5) A camada **services** manipula os registros do banco de dados.
  6) A camada **static** fica responsável pela implementação dos arquivos estáticos como os arquivos CSS e JavaScript.
  7) A camada **templates**, como sabido, implementa os arquivos HTML que serão utilizados pela view. Mas gostaríamos de ressaltar que fizemos um estudo para aglutinar os 5 métodos da **view** em 3 arquivos HTML. Proporcionando assim maior reaproveitamento de código. Fizemos ainda uma subdivisão da navbar e do footer, colocando-os dentro da pasta _frames. Assim o index.html fica mais organizado, abrindo ainda a possibilidade que ambos possam ser destacados da página principal de acordo com o interesse.
  8) A pasta **password** guarda os arquivos de configração do Django.

## Segurança

- Todas as rotas da aplicaçao estão protegidas e só podem ser acessadas mediante login.
- A aplicação está protegida contra SQL Injection.
- Um ponto fraco é que a rota que é passada ao usuário não pode ficar protegida, pois ele precisa acessá-la sem nenhuma senha. Entretanto, o id dessas rotas é um número hexadecimal de 32 dígitos o que dificulta muito que seja adivinhada.
- A autenticação é feita mediante a criação de sessões. Inicialmente cogitamos implementar também a autenticação por JWT para a API, mas, por hora, não julgamos necessário, visto que as requisições do JavaScript também estão sendo autenticadas pela sessão. Caso outro aplicativo viesse a consumir esta API, aí veríamos mais sentido na implementação.

## Atendimento dos requisitos   

1) **Geração da senha aleatória:**
   - O processo de geração de senha é feito no back-end pela aplicação **api**, que cria e valida uma string randômica com no mínimo 8 e no máximo 50 caracteres. Sendo obrigatória a presença de maiúsculas, minúsculas, números e caracteres especiais.
     - Quanto aos caracteres especiais selecionamos alguns manualmente tentando evitar alguns que sabidamente dão problemas em determinados contextos como '/' e '\\', mas para uma ação mais assertiva seria interessante fazer um estudo dos impactos nas aplicações para as quais as senhas estão sendo geradas.
   - O administrador do site pode determinar o tamanho da senha por um **input** do tipo **range** ou por um do tipo **number**. As alterações nesses campos são enviadas automaticamente para a API via JavaScript, visando uma melhor experiência do usuário, visto que as alterações acontecem em tempo real.
   - A senha é gerada assim que a página é carregada, mas há um botão **atualizar** que faz uma requisição para a API pelo JavaScript permitindo que o administrador do site possa gerar várias senhas até achar uma que considere mais amigável, se for do seu interesse.
2) **Expiração:**
   - O administrador pode determinar um número inteiro que determina o número de vezes que a senha pode ser visualizada.
   - Há uma verificação para que o administrador não se esqueça de preencher o campo do número de visualizações e da data de expiração da senha.
   - O administrador pode determinar uma data de expiração para a senha.
   - Há uma verificação para que o administrador não preencha o campo do número de visualizações com ZERO ou algum número negativo.
   - Há uma verificação para que o administrador não preencha a data de expiração em um dia no passado.
   - Melhorias e sugestões de melhorias:
     - Como muitas vezes esses valores são padronizados para todos os usuários, pensamos em fazer um preenchimento automático com valores default para esses campos, mas como isso não foi solicitado nos requisitos, não o fizemos. Preferimos optar por forçar o administrador a preenchê-los manualmente por entender que essa decisão talvez pode estar atrelada a alguma regra de segurança. Talvez o preenchimeto automático pudesse levar o administrador a definir por engano um prazo ou número de visualizações maior, gerando assim uma possível falha de segurança no aplicativo que vai usar a senha gerada. Mas deixamos isso pontuado para nosso gerente, caso julgue interessante fazer essa readequação.
     - Como a rota de visualização obrigatoriamente deve ficar exposta para ser acessada por qualquer um que receber o link, acrescentamos um registro dos acessos feitos, contendo a data e a hora em que o acesso foi feito, bem como o IP que realizou o acesso. Esse registro só pode ser visualizado pelos administradores do site. Isso também não estava nos requisitos, porém consideramos uma melhoria que só acrescenta ao projeto.
3) **A URL de visualização**
   - O sistema gera uma URL de acesso aberto com um número hexadecimal de 32 dígitos. Fizemos isso no intuito de impedir que as rotas possam ser adivinhadas facilmente.
   - Ao criar uma nova senha, o administrador é redirecionado para uma página onde pode verificar todos os dados persistidos no banco de dados.
   - Não sabemos como esse link será enviado. Se fosse por e-mail já implementaríamos um envio automático. Mas o texto dos requisitos sugere que pode ser enviada por várias ferramentas. Optamos então por copiar o link para o clipboard quando o administrador clica em cima do mesmo. Assim ele pode dar um Ctrl + V onde julgar necessário. Para uma ação mais assertiva e automatizada seria necessário realizar um estudo de quais ferramentas são utilizadas, sua documentação e APIs (se houver) e entender qual é o melhor processo de automatização.
   - A rota de visualização dos usuários (não logados) incrementa o número de visualizações. 
     - Obs1:: se a rota de visualização dos usuários for acessada por um administrador logado, não haverá incrementação da visualização.
     - Obs2::Os links da navbar só são visíveis nesta rota caso o administrador esteja logado.
4) **Bloqueio da senha**
    - Após atingir um dos dois critérios de expiração, o valor da senha é apagado no banco de dados assim que for feita uma nova requisição para visualizá-la.
    - Os outros dados como o link, o número de visualizações, a data de expiração e o registro dos acessos feitos permanece cadastrado no banco de dados.
      - Preferimos deixar assim por ser possível gerar uma auditoria dos acessos caso seja necessário. Sobretudo pelo registro de data/hora de acesso e IPs. Acreditamos fortemente que a auditoria apenas acrescenta segurança ao processo, mas isso poderia ser adequado mediante as decisões do gerente.
      - O administrador pode apagar o registro manualmente, bem como todos os acessos vinculados a ele.
      - O administrador pode apagar todos os registros que já expiraram.
        - Obs: Nós optamos por apagar apenas os registros cujo valor da senha está vazio e não a todos os registros que já atenderam a um dos critérios de expiração justamente para possibilitar a auditoria posterior. O que poderia ser facilmente readequado.
5) **Outras considerações**
    - Nós optamos por não vincular nenhum nome, e-mail ou data de criação por entender que isso são informações sensíveis. O ID hexadecimal é suficiente para unificar todas essas informações na medida em que será repassado pelo link de quem tentou acessar e teve algum problema. No entanto isso poderia facilmente ser readequado caso se julgue necessário ou melhore o uso pelo administrador do site.
    - Fizemos uma página onde o administrador pode visualizar todos os registros cadastrados. Por meio dessa página ele pode:
      - Acessar a página que mostra as informações detalhadas do registro, bem como os acessos realizados com data/hore e IP.
      - Copiar o link de visualização para o clipboard.
      - Apagar todos os registros de senha que estão em branco. (Campo value vazio)
