from postgreSQLRepo import PostgreSQLConnector, PostgreSQLOperations

def main():
    connector = PostgreSQLConnector()
    executer = PostgreSQLOperations(connector)
    # executer.select('Candidatos')
if __name__ == "__main__":
    main()