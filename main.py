from postgreSQLRepo import PostgreSQLConnector, PostgreSQLOperations
from menuRepo import ChoiceInteractor
from time import sleep
import os

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    connector = PostgreSQLConnector()
    executer = PostgreSQLOperations(connector)
    interactor = ChoiceInteractor(executer)
    print('Bem vindo!\n')
    while True:

        print('Digite o número da opção desejada:')
        print('1.Ver tabela')
        print('2.Remover dados')
        print('3.Encontrar candidaturas')
        print('4.Verificar candidatos ficha limpa')
        print('5.Gerar relatório de candidatos eleitos')
        print('6.Sair')

        choice = input()

        if choice not in ['1', '2', '3', '4', '5', '6']:
            print(f"\nO valor digitado '{choice}' não corresponde a nenhuma das opções, voltando ao menu inicial...")
            sleep(2.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            continue

        elif choice == '6':
            break

        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            response = interactor.execute_operation(int(choice))
            if not response:
                break
            os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    main()