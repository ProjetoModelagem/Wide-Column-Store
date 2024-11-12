# Projeto de Banco de Dados NoSQL com Astra DB

## Integrantes do Grupo
- **Guilherme de Abreu** - Matrícula: 22.222.028-7

## Projeto do semestre passado

- [Projeto](https://github.com/GuizinhoAB/Modelo-de-Banco-de-Dados/tree/main)

## Descrição do Projeto
Este projeto realiza a migração de dados de um banco de dados PostgreSQL para um banco de dados NoSQL, o Astra DB. Ele manipula informações de alunos, professores, cursos, departamentos, disciplinas e grupos de TCC, transferindo esses dados para coleções no Astra DB.

## Como Executar o Código

1. **Instalar Dependências:**
   - Para este projeto, recomendo usar a versão do Python 3.12, pois o `psycopg2` pode apresentar problemas com versões mais recentes.
   - Instale as bibliotecas necessárias com o seguinte comando:
     ```bash
     pip install psycopg2 astrapy
     ```

2. **Configurar o PostgreSQL e o Astra DB:**
   - **PostgreSQL**: Certifique-se de que o seu banco de dados PostgreSQL está funcionando corretamente, utilizando o pgAdmin para gerenciar o banco de dados.
   - **Astra DB**: Configure o Astra DB no [DataStax Astra Portal](https://astra.datastax.com/) e obtenha o token de autenticação.
   Com isso, coloque as informações nas variáveis nos códigos.
   ASTRA_DB_APPLICATION_TOKEN
   ASTRA_DB_API_ENDPOINT 
   ASTRA_DB_KEYSPACE


3. **Rodar o Script:**
   - Se quiser limpar as coleções no Astra DB, execute:
     ```bash
     python limpeza.py
     ```

   - Primeiro, popule o banco de dados relacional PostgreSQL:
     ```bash
     python criacao_tabela.py
     python data_generator.py
     ```

   - Em seguida, execute os scripts no terminal para criar, migrar e realizar as queries:
     ```bash
     python criacao_colecao.py
     python migracao.py
     python queries.py
     ```

## Queries para a Criação das Coleções Necessárias

- As queries para criar as coleções no Astra DB estão no arquivo **criacao_colecao.py**.

## Código Desenvolvido para Extrair os Dados do Banco Relacional

- O código de migração para o Astra DB está no arquivo **migracao.py**.

## Queries que Resolvem os 5 Itens

- As consultas que atendem aos requisitos específicos estão no arquivo **queries.py**.

## Validação das Queries

- Para garantir que os dados foram migrados corretamente, recomendo usar a interface do DataStax Astra Portal para verificar as coleções criadas.

## Descrição das Coleções

## Descrição das Coleções

1. **alunos**
   ```json
   {
     "_id": "350425d7-c84a-470b-8425-d7c84ab70bef",
     "id": "27",
     "nome": "Elisa da Rocha",
     "email": "jadeleao@example.org",
     "data_nascimento": "2003-11-17",
     "data_matricula": "2021-04-24",
     "situacao_graduacao": true,
     "historico_escolar": [
       {
         "disciplina_id": 9,
         "nome_disciplina": "Ortopedista",
         "semestre": 5,
         "ano": 2019,
         "nota_final": 3.9
       },
       {
         "disciplina_id": 15,
         "nome_disciplina": "Cantor",
         "semestre": 7,
         "ano": 2016,
         "nota_final": 4.92
       }
       // ...
     ],
     "tcc_grupo": null
  }
     ```

  2. **professores**
  ```json
     {
       "_id": "475098a1-cac1-4601-9098-a1cac1b6018c",
       "id": "6",
       "nome": "Noah Vasconcelos",
       "email": "julia96@example.net",
       "data_nascimento": "1977-10-30",
       "data_contratacao": "2024-10-08",
       "disciplinas_ministradas": [
         {
           "disciplina_id": 6,
           "nome_disciplina": "Paramédico",
           "semestre": 6,
           "ano": 2021
         }
         // ...
       ],
       "departamento": {
         "departamento_id": 1,
         "nome": "Matemática e Estatística",
         "chefe": false
       }
  }

  ```
   3. **grupos_tcc**
   ```json
  {
    "_id": "742243da-2e68-4d9c-a243-da2e686d9c42",
    "grupo_numero": 3
  }

  ```

   4. **disciplinas**
   ```json
  {
    "_id": "f0386f13-86d5-4448-b86f-1386d5b448c5",
    "id": "11",
    "nome": "Capitão"
  }

  ``` 

   5. **departamentos**
   ```json
  {
    "_id": "03e87f51-826c-4080-a87f-51826cc080fc",
    "id": "1",
    "nome": "Matemática e Estatística"
  }

  ```

   6. **cursos**
   ```json
  {
    "_id": "8abb1d0a-4557-4e1f-bb1d-0a45571e1f93",
    "id": "8",
    "nome": "Programador"
  }

```
