import psycopg2
from psycopg2 import OperationalError
from time import sleep

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

    def check_dataset_tables(self):
        sql = f"""SELECT table_name FROM information_schema.tables
                  WHERE table_schema = 'public'"""
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            results = None
            print('Nenhuma tabela encontrada!')
            
        return results

    def display_selection(self, table):
        sql = f"""SELECT * FROM {table}"""
        print(f'Executando seleção com a query: {sql}\n')
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            results = None
            
        if results:
            self.cursor.execute(f"Select * FROM {table} LIMIT 0")
            for column in self.cursor.description:
                print('|', column[0].upper().center(30), '|', end=' ')
            print('\n')
            print('-'*(len(self.cursor.description)*30 + len(self.cursor.description) + 15))
            for line in results:
                for field in line:
                    print('|', str(field).center(30), '|', end=' ')
                print('\n')
            sleep(5)


class ChoiceInteractor:

    def __init__(self, operator: PostgreSQLOperations):
        self.operator = operator

    def execute_operation(self, choice: int):
        if choice == 1:
            while True:
                print('Qual tabela você deseja visualizar?\n')
                results = self.operator.check_dataset_tables()
                option_assign = {}
                for index, line in enumerate(results):
                    option_assign[str(index+1)] = line[0]
                    print(str(index+1) + '.', line[0])
                print('\n', 'Digite 0 para retornar ao menu anterior, ou SAIR para encerrar o programa')
                table_choice = input().upper()
                if table_choice not in list(option_assign.keys()) + ['0', 'SAIR']:
                    print(f"\nO valor digitado '{choice}' não corresponde a nenhuma das opções, voltando ao menu...")
                    sleep(2.5)
                elif table_choice == '0':
                    return True
                elif table_choice == 'SAIR':
                    return False
                else:
                    self.operator.display_selection(option_assign[table_choice])
                    return True