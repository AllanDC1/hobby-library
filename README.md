# Hobby Library

Sistema web para cadastro de usuarios e hobbies, com suporte a campos dinâmicos por hobby e cache para melhorar desempenho das consultas.

## Tema escolhido

O tema do projeto é uma "biblioteca de hobbies" pessoal:

- O usuario cria sua conta e registra hobbies.
- Cada hobby pode ter atributos diferentes (exemplo: culinaria com receita favorita; ciclismo com distancia media).
- O sistema permite listar, detalhar, editar e remover hobbies.
- A ideia é ter um local para agrupar todos seus hobbies de maneira flexível


## Arquitetura

```
   Frontend (HTML/CSS/JS)
              |
     FastAPI (Python)
    +---------+--------+
    |         |        |
PostgreSQL  MongoDB  Redis
(Supabase) (Atlas)  (Upstash)
  Usuários  Hobbies   Cache
```

- O PostgreSQL (Supabase) foi escolhido para armazenar os usuários pela consistencia dos dados e facilitar validações como a unicidade de e-mails
- O MongoDB (Atlas) foi fundamental para a flexibilização dos campos dos hobbies por ser schemaless
- E o Redis (Upstash) foi usado para cache, acelerando a listagem de hobbies para o usuário


## Stack

| Camada   | Tecnologia          | Serviço Online |
|----------|---------------------|----------------|
| Frontend | HTML + CSS + JS     | —              |
| Backend  | Python + FastAPI    | —              |
| BD Relacional | PostgreSQL     | Supabase       |
| BD NoSQL | MongoDB             | MongoDB Atlas  |
| Cache (NoSQL) | Redis          | Upstash Redis  |

## Como rodar

### 0. Requisitos

- Python 3.14

### 1. Criar contas gratuitas

- **Supabase** (PostgreSQL): https://supabase.com
  - Crie um projeto → copie a URL e Publishable Key
  - No SQL Editor, execute o script `backend/database/schema.sql`

- **MongoDB Atlas**: https://www.mongodb.com/atlas
  - Crie um cluster gratuito
  - Crie um banco chamado `hobby_library`
  - Copie a connection string

- **Upstash Redis**: https://upstash.com
  - Crie um banco Redis gratuito
  - Copie a URL de conexão (com rediss://)

### 2. Configurar variáveis de ambiente

```bash
cd backend
copy .env.example .env
```

Edite o `.env` com suas credenciais.

### 3. Instalar dependências

```bash
cd backend
pip install -r requirements.txt
```

### 4. Rodar o servidor

```bash
cd backend
uvicorn main:app --reload
```

Acesse http://localhost:8000 para usar a aplicação.

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| POST   | `/api/users` | Criar/login de usuario |
| POST   | `/api/users/{id}/hobbies` | Adicionar hobby |
| GET    | `/api/users/{id}/hobbies` | Listar hobbies (com cache) |
| GET    | `/api/users/{id}/hobbies/{hobby_id}` | Detalhes de um hobby |
| PUT    | `/api/users/{id}/hobbies/{hobby_id}` | Editar hobby |
| DELETE | `/api/users/{id}/hobbies/{hobby_id}` | Remover hobby |

## Como funciona o cache

Quando o usuário lista seus hobbies:
1. O backend verifica se existe no **Redis**
2. Se sim → retorna do cache (resposta marcada como `⚡ cache`)
3. Se não → busca no **MongoDB** e salva no Redis por 5 minutos
4. Quando um hobby é criado, editado ou excluído → cache é invalidado

## Estrutura de um hobby no MongoDB

```json
{
    "_id": "ObjectId",
    "user_id": "uuid-do-postgres",
    "name": "Cozinhar",
    "category": "Culinária",
    "receita_favorita": "Lasanha",
    "nivel": "Intermediário",
    "anos_praticando": 5,
    "created_at": "2026-03-30T...",
    "updated_at": "2026-03-30T..."
}
```
