from postgreSQLRepo import PostgreSQLOperations
from time import sleep
import os

class ChoiceInteractor:

    def __init__(self, operator: PostgreSQLOperations):
        self.operator = operator

    def execute_operation(self, choice: int):
        if choice == 1:
            return self.run_selection()
        elif choice == 2:
            return self.run_deletion()
        elif choice == 3:
            raise NotImplementedError
        elif choice == 4:
            raise NotImplementedError
        elif choice == 5:
            raise NotImplementedError

    def run_selection(self):
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
                print(f"\nO valor digitado '{table_choice}' não corresponde a nenhuma das opções, voltando ao menu...")
                sleep(2.5)
            elif table_choice == '0':
                return True
            elif table_choice == 'SAIR':
                return False
            else:
                self.operator.display_selection(option_assign[table_choice])
                input('\nPressione qualquer tecla para voltar ao menu\n')
                os.system('cls' if os.name == 'nt' else 'clear')
    
    def run_deletion(self):
        while True:
            print("De qual tabela você deseja remover dados?")
            results = self.operator.check_dataset_tables()
            option_assign = {}
            for index, line in enumerate(results):
                option_assign[str(index+1)] = line[0]
                print(str(index+1) + '.', line[0])
            print('\n', 'Digite 0 para retornar ao menu anterior, ou SAIR para encerrar o programa')
            table_choice = input().upper()
            if table_choice not in list(option_assign.keys()) + ['0', 'SAIR']:
                print(f"\nO valor digitado '{table_choice}' não corresponde a nenhuma das opções, voltando ao menu...")
                sleep(2.5)
            elif table_choice == '0':
                return True
            elif table_choice == 'SAIR':
                return False
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                mode_choice = input('\nDigite 0 para deletar todos os dados da tabela, ou então digite o nome da coluna e o valor \
                                    da linha para ser deletada, separado por virgula:')
                if mode_choice == '0':
                    self.operator.delete_data(option_assign[table_choice])
                    input('\nPressione qualquer tecla para voltar ao menu\n')
                    os.system('cls' if os.name == 'nt' else 'clear')
                elif ',' not in mode_choice:
                    print('\nEntrada inválida. Certifique-se de que os campos estejam separados por vírgula\n')
                    sleep(2)
                else:
                    key = [i.strip(' ') for i in mode_choice.split(',')]
                    key[0] = key[0].lower()
                    self.operator.delete_data(option_assign[table_choice], key)
                    input('\nPressione qualquer tecla para voltar ao menu\n')
                    os.system('cls' if os.name == 'nt' else 'clear')