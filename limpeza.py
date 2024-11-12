from astrapy import DataAPIClient

# Configurações do Astra DB
ASTRA_DB_APPLICATION_TOKEN = "info"
ASTRA_DB_API_ENDPOINT = "info"
ASTRA_DB_KEYSPACE = "info"

# Inicializar o cliente Astra
client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
database = client.get_database(ASTRA_DB_API_ENDPOINT)

print(f"Conectado ao Astra DB: {ASTRA_DB_KEYSPACE}")

# Apaga todos os documentos na colecao
def limpar(collection_name):
    try:
        collection = database.get_collection(collection_name)
        documents = collection.find({})
        for document in documents:
            if collection_name == "grupos_tcc":
                collection.delete_one({"grupo_numero": document["grupo_numero"]})
            else:
                collection.delete_one({"id": document["id"]})
        print(f"Todos os documentos da coleção '{collection_name}' foram removidos com sucesso.")
    except Exception as e:
        print(f"Erro ao limpar a coleção '{collection_name}': {e}")

collections_to_clear = [
    "alunos",
    "professores",
    "cursos",
    "departamentos",
    "disciplinas",
    "grupos_tcc"
]

for collection_name in collections_to_clear:
    limpar(collection_name)

print("Todas as coleções foram limpas com sucesso.")
