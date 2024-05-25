import psycopg2
from psycopg2 import OperationalError
from time import sleep
import os

class PostgreSQLConnector:
    
    def __init__(self):
        self.connection = self.connect()

    def connect(self, host='localhost',  database='testdatabase', user='TestUser', password='test'):
        while True:
            try:
                connection = psycopg2.connect(host=host, database=database, user=user, password=password)
                print(f'Usuário {user} conectado com sucesso ao banco de dados {database}\n')
                return connection
            except OperationalError:
                print('Ocorreu um erro ao fazer a conexão com o banco de dados solicitado\n')
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
        os.system('cls' if os.name == 'nt' else 'clear')
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

    def delete_data(self, table, key=None):
        if key:
            try:
                value = float(key[1])
                sql = f"""DELETE FROM {table}
                      WHERE {key[0]} = {value}"""
            except ValueError:
                sql = f"""DELETE FROM {table}
                        WHERE {key[0]} = '{key[1]}'"""
        else:
            sql = f"""DELETE FROM {table}"""
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e
        self.connection.commit()
        print('Dados deletados com sucesso')

    def display_campaigns(self, filters = None, order=None):
        where = ''
        if 'Ano' in filters.keys():
            where += f"cd.ano = {filters['Ano']} AND "
        
        if 'Nome do candidato' in filters.keys():
            where += f"i.nome = '{filters['Nome do candidato'].title()}' AND "

        if 'Cargo' in filters.keys():
            where += f"cg.nome = '{filters['Cargo'].title()}' AND "

        sql = f"""SELECT cd.cpf, i.nome, cd.numero_candidato, cd.partido_id, cg.nome, cd.ano, cd.ficha_limpa
                  FROM candidato cd
                  JOIN individuos i
                  ON cd.cpf = i.cpf
                  LEFT JOIN cargos cg
                  ON cd.cargo_id = cg.cargo_id
                  WHERE {where}"""
        sql = sql.strip('\n').strip(' AND ')

        order_assign = {'1': '\nORDER BY cd.ano ASC',
                        '2': '\nORDER BY cd.ano DESC',
                        '3': '\nORDER BY i.nome ASC',
                        '4': '\nORDER BY i.nome DESC',
                        '5': '\nORDER BY cg.nome ASC',
                        '6': '\nORDER BY cg.nome DESC'}
        
        if order:
            sql += order_assign[order]

        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            results = None

        os.system('cls' if os.name == 'nt' else 'clear')
        print('|', 'CPF'.center(13), '|', 'NOME'.center(30), '|', 'NUMERO'.center(5), '|',
              'PARTIDO'.center(5), '|', 'CARGO'.center(20), '|', 'ANO'.center(6), '|',
              'FICHA_LIMPA'.center(7), '|')
        print('-'*115)

        spacing = [13, 30, 5, 5, 20, 6, 7]

        if results:
            for line in results:
                for field, space in zip(line, spacing):
                    print('| ', str(field).center(space), end=' ')
                print('\n')

    def save_elected_report(self):        
        sql = f"""SELECT 
                    cd.candidato_id,
                    i.nome,
                    cd.vice_candidato_id AS id_vice,
                    p.pleito_id,
                    c.nome_cargo,
                    v.quantidade_votos,
                    c.quantidade_eleitos,
                    (ROW_NUMBER() OVER (PARTITION BY v.cargo_id ORDER BY v.quantidade_votos DESC) <= c.quantidade_eleitos) AS eleito
                FROM 
                    candidato cd
                LEFT JOIN 
                    vice_candidato vc ON cd.vice_candidato_id = vc.vice_candidato_id
                JOIN 
                    individuos i on cd.cpf = i.cpf
                JOIN 
                    pleitos p ON cd.pleito_id = p.pleito_id
                JOIN 
                    votacao v ON cd.candidato_id = v.candidato_id
                JOIN 
                    cargos c ON v.cargo_id = c.cargo_id 
                WHERE eleito = TRUE
                ORDER BY 
                    v.cargo_id, v.quantidade_votos DESC"""
        
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            results = None
        
        # results = [(13, 'zé minino', '123', '34', 'prefeito', '54', '1', True),
        #             (21, 'zé moço', '321', '35', 'vereador', '99', '7', True)]

        if results:
            with open('reports/eleitos.txt', 'w') as file:
                file.write('CANDIDATOS ELEITOS:\n')
                line_to_write = "| {} | {} | {} | {} | {} | {} | {} |".format(
                                                                                'ID'.center(10),
                                                                                'NOME'.center(30),
                                                                                'ID_VICE'.center(10),
                                                                                'ID_PLEITO'.center(10),
                                                                                'CARGO'.center(15),
                                                                                'VOTOS'.center(7),
                                                                                'ELEITOS'.center(9)
                                                                            )
                file.write(line_to_write)
                file.write('\n')
                file.write('-'*115)
                file.write('\n')
                spacing = [10, 30, 10, 10, 15, 7, 9]
                for line in results:
                    line = line[0:-1]
                    file.write('| ')
                    for field, space in zip(line, spacing):
                        file.write(f"{str(field).center(space)}")
                        file.write(' | ')
                    file.write('\n')
        self.connection.commit()

    def display_ficha_limpa(self):
        sql = f"""SELECT cpf, nome,
                  FROM individuos
                  WHERE ficha_limpa = TRUE"""
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            results = None

        os.system('cls' if os.name == 'nt' else 'clear')

        print('LISTAGEM DE INDIVÍDUOS COM A FICHA LIMPA:')
        print('|', 'CPF'.center(13), '|', 'NOME'.center(30), '|')
        spacing = [13, 30]
        if results:
            for line in results:
                for field, space in zip(line, spacing):
                    print('| ', str(field).center(space), end=' ')
                    print('\n')
        self.connection.commit()