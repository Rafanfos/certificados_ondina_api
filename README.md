# Certificados Ondina API  

O **Certificados Ondina API** é o backend responsável por gerenciar os dados e fornecer serviços para a geração de certificados e diplomas. Ele foi desenvolvido em **Django** e oferece suporte tanto para execução local quanto via **Docker**.  

---

## Instalação  

### Pré-requisitos  

Antes de começar, certifique-se de ter instalado os seguintes softwares:  

1. **Python** (versão 3.8 ou superior).  
2. **PostgreSQL** (versão 12 ou superior).  
3. **Docker** e **Docker Compose** (opcional, para execução via contêineres).  

---

### Configuração do Banco de Dados  

Para configurar o banco de dados **PostgreSQL**, você tem três opções: utilizando o terminal com `psql`, ou por meio das interfaces gráficas **pgAdmin** ou **DBeaver**.

#### **Opção 1: Usando o terminal (`psql`)**

1. Abra o terminal ou o shell do PostgreSQL com o comando:  

    ```bash
    psql -U postgres
    ```

2. Após acessar o shell do PostgreSQL, crie um novo banco de dados executando o seguinte comando:

    ```sql
    CREATE DATABASE certificados_ondina;
    ```

3. Crie um usuário para o banco de dados (se necessário) com o comando:

    ```sql
    CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
    ```
  
4. Conceda as permissões necessárias para o banco de dados ao usuário criado:

    ```sql
    GRANT ALL PRIVILEGES ON DATABASE certificados_ondina TO seu_usuario;
    ```

5. Para verificar se o banco de dados foi criado corretamente, use o comando:

    ```sql
    \l
    ```

6. Isso mostrará uma lista de bancos de dados disponíveis.

#### **Opção 2: Usando pgAdmin**

1. Abra o pgAdmin e conecte-se ao servidor PostgreSQL.

2. Clique com o botão direito sobre o servidor e selecione Create > Database.

3. Preencha o nome do banco de dados como certificados_ondina e clique em Save.

4. Para criar um novo usuário, vá até Login/Group Roles e clique com o botão direito em Create > Login/Group Role. Preencha os dados do usuário e forneça uma senha.

5. Para conceder permissões ao novo usuário, vá até o banco de dados certificados_ondina, clique em Properties > Security e adicione o usuário com permissões adequadas.

#### **Opção 3: Usando DBeaver**

1. Abra o DBeaver e conecte-se ao seu servidor PostgreSQL.

2. Na seção Database Navigator, clique com o botão direito sobre Databases e selecione Create > Database.

3. No campo de nome, digite certificados_ondina e clique em OK.

Para criar um usuário, clique com o botão direito sobre Roles e selecione Create New Role. Preencha as informações do usuário e conceda permissões para o banco de dados criado.

### Configuração das Variáveis de Ambiente

Após criar o banco de dados, você precisará configurar as variáveis de ambiente.

1. Copie o arquivo .env.example para .env na raiz do projeto.
2. Edite o arquivo .env e preencha com as informações do seu ambiente:

    ```env
    ENV=development
    DEBUG=True
    SECRET_KEY=seu_secret_key_aqui

    # Configuração do banco de dados
    DB_NAME=certificados_ondina
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_HOST=localhost
    DB_PORT=5432
    ```

### Rodando o projeto

#### Opção 1: Executando com Python

1. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

2. Realize as migrações do banco de dados:

    ```bash
    Copiar código
    python manage.py migrate
    ```

3. Crie um superusuário para gerenciar o sistema:

    ```bash
    python manage.py createsuperuser
    ```

4. Inicie o servidor de desenvolvimento:

    ```bash
    python manage.py runserver
    ```

O servidor estará disponível em <http://localhost:8000>.

#### **Opção 2: Executando com Docker**

1. Escolha o arquivo Docker Compose de acordo com o ambiente:

   - Para desenvolvimento ou staging, use docker-compose-dev.yml.
   - Para produção, use docker-compose.yml.

2. Suba os contêineres:

    ```bash
    docker-compose -f docker-compose-dev.yml up --build
    ```

O servidor estará disponível em <http://localhost:3030>.

## Criando Usuários

1. Criar Superusuário

    Para criar um superusuário, use o comando:

    ```bash
    python manage.py createsuperuser
    ```

2. Autenticação via API

    Use a rota de login para autenticar com o superusuário:

    ```bash
    POST /api/users/login
    ```

3. A requisição deve enviar as credenciais do superusuário no corpo (em formato JSON) que pode ser feita utilizando Insonmia ou Postman:

    ```json
    {
        "username": "seu_usuario",
        "password": "sua_senha"
    }
    ```

4. Criar Usuários pela API:

    Após estar autenticado como superusuário, use a rota para registrar novos usuários:

    ```bash
    POST /api/users/register
    ```

Certifique-se de enviar as credenciais de autenticação do superusuário no cabeçalho da requisição.

## Endpoints

### 1. **Registro de Usuário**

Essa rota cria um usuário no banco de dados da aplicação.

- **Método:** `POST`
- **Rota:** `/api/users/register`

- **Body da Requisição**

    ```json
    {
        "username": "seu_usuario",
        "email": "seu_email@mail.com",
        "first_name": "Seu Nome",
        "last_name": "Seu Sobrenome",
        "password": "sua_senha"
    }
    ```

- **Resposta**

    ```json
    {
        "id": "cc31e951-8b86-4546-bc6c-1b6909fe9e45",
        "username": "diretoria_ondina",
        "email": "diretoria_ondina@mail.com",
        "first_name": "Diretoria",
        "last_name": "Ondina",
        "is_superuser": false
    }
    ```

### 2. Login do usuário

Esta rota autentica um usuário já cadastro no sistema.

- **Método:** `POST`
- **Rota:** `/api/users/login`

- **Body da Requisição**

    ```json
    {
        "username": "seu_usuario",
        "password": "sua_senha"
    }
    ```

- **Resposta**

    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNDQ1MDY3NCwiaWF0IjoxNzMzODQ1ODc0LCJqdGkiOiJkYzQxOTUwZjgwMDM0MWRjOWFiOWQwNWFkZGI1ZmM1MiIsInVzZXJfaWQiOiJjYzMxZTk1MS04Yjg2LTQ1NDYtYmM2Yy0xYjY5MDlmZTllNDUifQ.WqyJMx8uMeWoGpXM1giUibLgIMrNeVddH0kTd7tpV0k",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzODk5ODc0LCJpYXQiOjE3MzM4NDU4NzQsImp0aSI6IjE3ZmNlNDQ4NWRhOTRmNDU5ZjBiNWQzZmExN2Y1MzMyIiwidXNlcl9pZCI6ImNjMzFlOTUxLThiODYtNDU0Ni1iYzZjLTFiNjkwOWZlOWU0NSJ9.aTCK9vDfZzWiAavjkpdlJWLE8mgd6tHQgXE4mPsn03U"
    }
    ```

### 3. Listar Alunos

Esta rota lista todos os alunos com suas informações de nome trimestre, e se foram gerados seus certificados de destaque e/ou diplomas.

- **Método:** `GET`
- **Rota:** `/api/students/list`
- **Autenticação:** O Bearer token deve ser enviado no cabeçalho da requisição

    ```makefile
    Authorization: Bearer <seu_token_aqui>
    ```

- **Resposta**

    ```json
    {
        "students": [
            {
                "id": "ff89acf7-d775-4459-9696-024676df13a1",
                "full_name": "LUANA RIBEIRO LOPES",
                "graduation_term": "3",
                "diploma_generated": true,
                "highlight_certificate_generated": false
            },
            {
                "id": "0dc1aea8-0cdf-4647-8831-caa7c67c8819",
                "full_name": "JOAO PEDRO OLIVEIRA SANTOS DA SILVA",
                "graduation_term": "3",
                "diploma_generated": true,
                "highlight_certificate_generated": false
            }
        ]
    }
    ```

### 4. **Registro de Alunos**

Essa rota permite o registro de alunos por meio do upload de um arquivo CSV com os dados dos alunos.

- **Método:** `POST`
- **Rota:** `/api/students/register`
- **Body de requisição:**

    ```csv
    nome completo,trimestre
    João Silva,1
    Maria Souza,2
    Pedro Oliveira,3
    ```

- **Resposta:**

    ```json
    {
        "message": "Alunos registrados com sucesso.",
        "students": [
            {
                "id": "ff89acf7-d775-4459-9696-024676df13a1",
                "full_name": "João Silva",
                "graduation_term": "1"
            },
            {
                "id": "0dc1aea8-0cdf-4647-8831-caa7c67c8819",
                "full_name": "Maria Souza",
                "graduation_term": "2"
            },
            {
                "id": "9fb2a64c-d50f-4725-a474-2e4c0a5445f6",
                "full_name": "Pedro Oliveira",
                "graduation_term": "3"
            }
        ]
    }
    ```

### 5. **Gerar Certificado ou Diploma**

Essa rota permite gerar um certificado ou diploma para um aluno. O tipo de certificado pode ser um "highlight certificate" ou um "diploma". A requisição inclui informações do aluno e os nomes do diretor e vice-diretor (se necessário).

- **Método:** `POST`
- **Rota:** `/api/students/generate-certificate`
- **Body da Requisição(certificado de destaque):**

    ```json
    {
        "certificate_type": "highlight_certificate",
        "student_id": "219cf842-35df-445a-ab50-d4f2de3a62e9",
        "director": "Rafael",
        "vice_director": "Gabriel"
    }
    ```

- **Corpo da Requisição (diploma):**

    ```json
    {
        "certificate_type": "highlight_certificate",
        "student_id": "219cf842-35df-445a-ab50-d4f2de3a62e9",
        "director": "Rafael",
   
    }
    ```

- **Resposta:**

    ```http
    HTTP/1.1 200 OK
    Content-Type: application/pdf
    Content-Disposition: attachment; filename="certificate.pdf"
    ```

O arquivo PDF será retornado diretamente no corpo da resposta. O cliente poderá então salvar o arquivo no seu sistema.

- **Mensagens de Erro:**

  1. **Aluno não encontrado (404):** Caso o student_id fornecido não corresponda a um aluno existente, a resposta será:

      ```json
      {
          "error": "Student not found"
      }
      ```

  2. **Tipo de certificado inválido (404):** Caso o certificate_type fornecido não seja válido (ou seja, não seja "highlight_certificate" ou "diploma"), a resposta será:

      ```json
      {
          "error": "Invalid certificate type"
      }
      ```

**Observações:**

- Certificados "highlight_certificate" podem ser gerados para alunos que se destacaram.
- Diplomas exigem apenas o nome do diretor, sem a necessidade de vice-diretor.
- O sistema irá validar o student_id e garantir que o aluno existe na base de dados antes de gerar o certificado ou diploma.
