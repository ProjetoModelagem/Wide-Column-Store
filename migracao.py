from datetime import datetime
import psycopg2
from astrapy import DataAPIClient

# Configurações do Astra DB
ASTRA_DB_APPLICATION_TOKEN = "info"
ASTRA_DB_API_ENDPOINT = "info"
ASTRA_DB_KEYSPACE = "info"

# Inicializar o cliente Astra
client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
database = client.get_database(ASTRA_DB_API_ENDPOINT)

print(f"Conectado ao Astra DB: {ASTRA_DB_KEYSPACE}")

# Conexão com o PostgreSQL
pg_conn = psycopg2.connect(
        database="info",
        user="info",
        password="info",
        host="info",
        port="info"
)
pg_cursor = pg_conn.cursor()

# inserir dados no Astra DB
def inserir_astra(collection_name, document):
    try:
        collection = database.get_collection(collection_name)
        collection.insert_one(document)
        print(f"Documento inserido com sucesso na coleção '{collection_name}'.")
    except Exception as e:
        print(f"Erro ao inserir documento na coleção '{collection_name}': {e}")


# Mgrar alunos
def migrar_alunos():
    pg_cursor.execute("SELECT * FROM alunos;")
    alunos = pg_cursor.fetchall()
    for aluno in alunos:
        aluno_id = aluno[0]
        nome = aluno[1]
        email = aluno[2]
        data_nascimento = aluno[3].isoformat()
        data_matricula = aluno[4].isoformat()
        situacao_graduacao = aluno[5]

        # Obtem o historico escolar do aluno
        pg_cursor.execute("""
            SELECT he.disciplina_id, d.nome, he.semestre, he.ano, he.nota_final
            FROM historico_escolar he
            JOIN disciplinas d ON he.disciplina_id = d.id
            WHERE he.aluno_id = %s;
        """, (aluno_id,))
        historico = [
            {
                "disciplina_id": registro[0],
                "nome_disciplina": registro[1],
                "semestre": registro[2],
                "ano": registro[3],
                "nota_final": registro[4]
            }
            for registro in pg_cursor.fetchall()
        ]

        # Obtem info de TCC, se tiver
        pg_cursor.execute("""
            SELECT grupo, professor_orientador_id
            FROM grupo_tcc
            WHERE aluno_id = %s;
        """, (aluno_id,))
        tcc_info = pg_cursor.fetchone()
        tcc_grupo = None
        if tcc_info:
            grupo_numero = tcc_info[0]
            orientador_id = tcc_info[1]

            # Obtem nome do orientador
            pg_cursor.execute("SELECT nome FROM professores WHERE id = %s;", (orientador_id,))
            orientador_nome = pg_cursor.fetchone()[0]
            tcc_grupo = {
                "grupo_numero": grupo_numero,
                "orientador_id": orientador_id,
                "orientador_nome": orientador_nome
            }

        aluno_doc = {
            "id": str(aluno_id),
            "nome": nome,
            "email": email,
            "data_nascimento": data_nascimento,
            "data_matricula": data_matricula,
            "situacao_graduacao": situacao_graduacao,
            "historico_escolar": historico,
            "tcc_grupo": tcc_grupo
        }

        inserir_astra("alunos", aluno_doc)


# Migrar professores
def migrar_professores():
    pg_cursor.execute("SELECT * FROM professores;")
    professores = pg_cursor.fetchall()
    for professor in professores:
        professor_id = professor[0]
        nome = professor[1]
        email = professor[2]
        data_nascimento = professor[3].isoformat()
        data_contratacao = professor[4].isoformat()

        # Obtem historico de disciplinas ministradas
        pg_cursor.execute("""
            SELECT hdp.disciplina_id, d.nome, hdp.semestre, hdp.ano
            FROM historico_disciplina_professores hdp
            JOIN disciplinas d ON hdp.disciplina_id = d.id
            WHERE hdp.professor_id = %s;
        """, (professor_id,))
        disciplinas_ministradas = [
            {
                "disciplina_id": registro[0],
                "nome_disciplina": registro[1],
                "semestre": registro[2],
                "ano": registro[3]
            }
            for registro in pg_cursor.fetchall()
        ]

        # Obtem o departamento e se o professor é chefe
        pg_cursor.execute("""
            SELECT d.id, d.nome, CASE WHEN pd.professor_id IS NOT NULL THEN true ELSE false END AS chefe
            FROM departamentos d
            LEFT JOIN professores_departamentos pd ON d.id = pd.departamento_id AND pd.professor_id = %s;
        """, (professor_id,))
        departamento = pg_cursor.fetchone()
        departamento_info = {
            "departamento_id": departamento[0],
            "nome": departamento[1],
            "chefe": departamento[2]
        }

        professor_doc = {
            "id": str(professor_id),
            "nome": nome,
            "email": email,
            "data_nascimento": data_nascimento,
            "data_contratacao": data_contratacao,
            "disciplinas_ministradas": disciplinas_ministradas,
            "departamento": departamento_info
        }

        inserir_astra("professores", professor_doc)

# Migrar cursos
def migrar_cursos():
    pg_cursor.execute("SELECT * FROM cursos;")
    cursos = pg_cursor.fetchall()
    for curso in cursos:
        curso_doc = {
            "id": str(curso[0]),
            "nome": curso[1]
        }
        inserir_astra("cursos", curso_doc)

# Migrar departamentos
def migrar_departamentos():
    pg_cursor.execute("SELECT * FROM departamentos;")
    departamentos = pg_cursor.fetchall()
    for departamento in departamentos:
        departamento_doc = {
            "id": str(departamento[0]),
            "nome": departamento[1]
        }
        inserir_astra("departamentos", departamento_doc)

# Migrar disciplinas
def migrar_disciplinas():
    pg_cursor.execute("SELECT * FROM disciplinas;")
    disciplinas = pg_cursor.fetchall()
    for disciplina in disciplinas:
        disciplina_doc = {
            "id": str(disciplina[0]),
            "nome": disciplina[1]
        }
        inserir_astra("disciplinas", disciplina_doc)

# Migrar grupos de TCC
def migrar_grupos_tcc():
    pg_cursor.execute("SELECT DISTINCT grupo FROM grupo_tcc;")
    grupos = pg_cursor.fetchall()
    for grupo in grupos:
        grupo_doc = {
            "grupo_numero": grupo[0]
        }
        inserir_astra("grupos_tcc", grupo_doc)


migrar_alunos()
migrar_professores()
migrar_cursos()
migrar_departamentos()
migrar_disciplinas()
migrar_grupos_tcc()

print("Migração concluída com sucesso!")
