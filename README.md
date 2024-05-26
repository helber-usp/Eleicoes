## Configuração do postgreSQL

O programa espera um banco de dados com as seguintes configurações:

- Nome do database: testdatabase
- Nome de usuário: TestUser
- Senha: test
- Porta: Não está definido no código, pois espera-se que use a porta padrão (5432)

### Obs: Esses parâmetros foram repetidos do exemplo em java visto em aula, portanto caso o database já esteja criado e com dados, esse programa pode mesclar informações de maneira indesejada.

Caso ocorra um problema de conexão devido a esses parâmetros não estarem de acordo, o programa irá permitir que o usuário insira os campos corretos interativamente.

## Ambiente

Todas os teste foram feitos com a versão do Python 3.10.14
O único pacote externo exigido para rodar o código é o psycopg2 (versão usada = 2.9.3)

## Execução

Para executar o programa, basta executar o arquivo main.py com o comando "python main.py" (ou "python3 main.py", dependendo do sistema)
