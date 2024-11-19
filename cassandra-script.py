import psycopg
import asyncio
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# Conectar ao PostgreSQL
def connect_postgres():
    try:
        conn = psycopg.connect('postgresql://postgres:senha123@localhost:5432/projeto2')
        print("Conexão com PostgreSQL estabelecida com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro na conexão com PostgreSQL: {e}")
        return None

# Conectar ao Cassandra usando asyncio
async def connect_cassandra():
    try:
        cluster = Cluster(['localhost'])  # Pode incluir vários nós
        session = cluster.connect('projeto')  # Nome do keyspace
        print("Conexão com Cassandra estabelecida com sucesso!")
        return session
    except Exception as e:
        print(f"Erro na conexão com Cassandra: {e}")
        return None

# Mapeamento de tipos PostgreSQL para Cassandra
def convert_postgres_type_to_cassandra(postgres_type):
    type_mapping = {
        'integer': 'int',
        'text': 'text',
        'decimal': 'decimal',
        'numeric': 'decimal',
        'boolean': 'boolean'
    }
    return type_mapping.get(postgres_type, 'text')

# Obtenção e conversão das tabelas
def get_postgres_table_structure(connection, table_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, (table_name,))
            columns = cursor.fetchall()
        
        if not columns:
            print(f"Aviso: Nenhuma coluna encontrada para a tabela '{table_name}'. Verifique se o nome está correto.")
        
        print(f"Estrutura da tabela '{table_name}': {columns}")
        return columns
    
    except Exception as e:
        print(f"Erro ao obter estrutura da tabela '{table_name}': {e}")
        return []

# Gerar CQL de criação da tabela no Cassandra
def create_cassandra_table(session, table_name, columns, primary_key):
    cql_query = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    
    for column_name, data_type in columns:
        cassandra_type = convert_postgres_type_to_cassandra(data_type)
        cql_query += f"    {column_name} {cassandra_type},\n"

    if primary_key:
        cql_query += f"    PRIMARY KEY ({', '.join(primary_key)})\n"
    else:
        print(f"Aviso: Nenhuma chave primária definida para a tabela {table_name}.")
        return

    cql_query += ");"
    
    try:
        session.execute(cql_query)
        print(f"Tabela {table_name} criada com sucesso no Cassandra.")
    except Exception as e:
        print(f"Erro ao criar tabela {table_name} no Cassandra: {e}")

# Migrar dados reais do PostgreSQL para Cassandra
def migrate_data(postgres_conn, cassandra_session, table_name, columns):
    try:
        with postgres_conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in rows:
                column_names = ', '.join([col[0] for col in columns])
                placeholders = ', '.join(['%s'] * len(columns))
                cql_insert = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
                cassandra_session.execute(cql_insert, row)
            print(f"Dados da tabela {table_name} migrados com sucesso!")
    
    except Exception as e:
        print(f"Erro ao migrar dados da tabela {table_name}: {e}")

# Estrutura das tabelas do PostgreSQL com suas chaves primárias
tables = {
    'curso': ['id_curso'],
    'aluno': ['ra'],
    'disciplina': ['codigo_disc'],
    'matrizcurricular': ['id_matriz', 'codigo_disc'],
    'histesc': ['ra', 'codigo_disc'],
    'histdisc': ['codigo_prof', 'codigo_disc'],
    'departamento': ['codigo_dep'],
    'professor': ['codigo_prof'],
    'formados': ['ra', 'id_matriz'],
    'tcc': ['id_tcc'],
    'historico_aluno': ['ra', 'codigo_disc'],
    'historico_prof': ['codigo_prof'],
    'chef_dep': ['codigo_prof'],
    'grupos_tcc': ['id'],
    'alunos_formados': ['ra', 'id_matriz', 'id_curso']
}

# Função principal para executar a migração
async def main():
    # Conectar ao PostgreSQL
    postgres_conn = connect_postgres()
    cassandra_session = await connect_cassandra()

    if postgres_conn and cassandra_session:
        for table_name, primary_key in tables.items():
            columns = get_postgres_table_structure(postgres_conn, table_name)
            create_cassandra_table(cassandra_session, table_name, columns, primary_key)
            migrate_data(postgres_conn, cassandra_session, table_name, columns)
        
        # Fechar a conexão ao final
        postgres_conn.close()
        cassandra_session.shutdown()

# Executar a função principal
if __name__ == "__main__":
    asyncio.run(main())
