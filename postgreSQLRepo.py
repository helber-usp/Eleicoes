import psycopg2
from psycopg2 import OperationalError

class PostgreSQLConnector:
    
    def __init__(self):
        self.connection = self.connect()

    def connect(self, host='localhost',  database='testdatabase', user='TestUser', password='test'):
        while True:
            try:
                connection = psycopg2.connect(host=host, database=database, user=user, password=password)
                print(f'Usuário {user} conectado com sucesso ao banco de dados {database}')
                return connection
            except OperationalError:
                print('Ocorreu um erro ao fazer a conexão com o banco de dados solicitado')
                esc = int(input('Digite 1 para tentar novamente, 2 para inserir os parâmetros de conexão manualmente, '\
                                'ou entre qualquer outra tecla para encerrar a aplicação.\n'))
                if esc not in [1, 2]:
                    print('Programa encerrado')
                    return None
                elif esc == 2:
                    host = input('Nome do host:')
                    database = input('Nome do database:')
                    user = input('Nome de usuário:')
                    password = input('Senha:')
                


class PostgreSQLOperations:

    def __init__(self, connector: PostgreSQLConnector):
        self.connection = connector.connection
        self.cursor = self.connection.cursor()

    def select(self, table):
        sql = f"""SELECT * FROM {table}"""
        print(f'Executando seleção com a query: {sql}')
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            results = None
            
        if results:
            for line in results:
                print(line)     