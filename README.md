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
    POST http://localhost:8000/api/users/login
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
    POST http://localhost:8000/api/users/register
    ```

Certifique-se de enviar as credenciais de autenticação do superusuário no cabeçalho da requisição.
