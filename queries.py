import random
from astrapy import DataAPIClient

# Configurações do Astra DB
ASTRA_DB_APPLICATION_TOKEN = "info"
ASTRA_DB_API_ENDPOINT = "info"
ASTRA_DB_KEYSPACE = "info"

# Inicializar o cliente Astra
client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
database = client.get_database(ASTRA_DB_API_ENDPOINT)

print(f"Conectado ao Astra DB: {ASTRA_DB_KEYSPACE}")


# Query que resolve o 1
def historico_escolar_aleatorio():
    collection = database.get_collection("alunos")
    documents = list(collection.find({})) 
    if not documents:
        print("Nenhum aluno encontrado.")
        return

    aluno = random.choice(documents)  # Seleciona um documento aleatorio
    nome = aluno.get("nome")
    historico = aluno.get("historico_escolar", [])

    print(f"\nHistórico escolar de {nome}:")
    if not historico:
        print("Nenhum histórico escolar encontrado.")
    else:
        for disciplina in historico:
            print(f"Código: {disciplina['disciplina_id']}, Nome: {disciplina['nome_disciplina']}, Semestre: {disciplina['semestre']}, Ano: {disciplina['ano']}, Nota Final: {disciplina['nota_final']}")


# Query que resolve o 2
def historico_professor_aleatorio():
    collection = database.get_collection("professores")
    documents = list(collection.find({}))  
    if not documents:
        print("Nenhum professor encontrado.")
        return

    professor = random.choice(documents)  # Seleciona um documento aleatório
    nome = professor.get("nome")
    disciplinas_ministradas = professor.get("disciplinas_ministradas", [])

    print(f"\nHistórico de disciplinas ministradas por {nome}:")
    if not disciplinas_ministradas:
        print("Nenhum histórico de disciplinas ministradas encontrado.")
    else:
        for disciplina in disciplinas_ministradas:
            print(f"Disciplina: {disciplina['nome_disciplina']}, Semestre: {disciplina['semestre']}, Ano: {disciplina['ano']}")


# Query que resolve o 3
def alunos_formados(semestre, ano):
    collection = database.get_collection("alunos")
    documents = collection.find({"situacao_graduacao": True})

    print(f"\nAlunos formados no semestre {semestre} do ano {ano}:")
    for doc in documents:
        nome = doc.get("nome")
        historico = doc.get("historico_escolar", [])
        disciplinas_aprovadas = [
            disc for disc in historico
            if disc["semestre"] == semestre and disc["ano"] == ano and disc["nota_final"] >= 6.0
        ]
        if disciplinas_aprovadas:
            print(f"- {nome}")


# Query que resolve o 4
def chefes_departamento():
    collection = database.get_collection("professores")
    documents = collection.find({})

    print("\nProfessores que são chefes de departamento:")
    found = False
    for doc in documents:
        departamento_info = doc.get("departamento", {})
        if departamento_info.get("chefe"):
            found = True
            nome_professor = doc.get("nome")
            nome_departamento = departamento_info.get("nome")
            print(f"Departamento: {nome_departamento}, Chefe: {nome_professor}")

    if not found:
        print("Nenhum chefe de departamento encontrado.")


# Query que resolve o 5
def grupo_tcc_info(group_num):
    collection = database.get_collection("alunos")
    documents = collection.find({"tcc_grupo.grupo_numero": group_num})

    print(f"\nGrupo de TCC número {group_num}:")
    orientador = None
    alunos = []

    for doc in documents:
        if not orientador:
            tcc_grupo = doc.get("tcc_grupo", {})
            orientador = tcc_grupo.get("orientador_nome")
        alunos.append(doc.get("nome"))

    if orientador:
        print(f"Orientador: {orientador}")
    else:
        print("Orientador não encontrado.")

    if alunos:
        print("\nAlunos:")
        for aluno in alunos:
            print(f"- {aluno}")
    else:
        print("Nenhum aluno encontrado.")


historico_escolar_aleatorio()
historico_professor_aleatorio()
alunos_formados(1, 2024)
chefes_departamento()
grupo_tcc_info(2)
