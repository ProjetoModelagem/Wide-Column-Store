from astrapy import DataAPIClient

# Configurações do Astra DB
ASTRA_DB_APPLICATION_TOKEN = "info"
ASTRA_DB_API_ENDPOINT = "info"
ASTRA_DB_KEYSPACE = "info"

# Inicializar o cliente Astra
client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
database = client.get_database(ASTRA_DB_API_ENDPOINT)

print(f"Conectado ao Astra DB: {ASTRA_DB_KEYSPACE}")

# criar coleções
def criar():
    collections_to_create = [
        "alunos",
        "cursos",
        "departamentos",
        "disciplinas",
        "grupos_tcc",
        "professores"
    ]

    for collection_name in collections_to_create:
        try:
            # Criar a coleção se ela não existir
            collection = database.create_collection(collection_name)
            print(f"Coleção '{collection_name}' criada com sucesso.")
        except Exception as e:
            print(f"Erro ao criar a coleção '{collection_name}': {e}")


criar()
