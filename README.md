# Hobby Library 📚

Biblioteca pessoal de hobbies com backend em FastAPI e 3 bancos de dados.

## Arquitetura

```
Frontend (HTML/CSS/JS)
         │
    FastAPI (Python)
    ┌────┼────────┐
    │    │        │
PostgreSQL  MongoDB  Redis
(Supabase) (Atlas)  (Upstash)
  Usuários  Hobbies   Cache
```

## Stack

| Camada   | Tecnologia          | Serviço Online |
|----------|---------------------|----------------|
| Frontend | HTML + CSS + JS     | —              |
| Backend  | Python + FastAPI    | —              |
| BD Relacional | PostgreSQL     | Supabase       |
| BD NoSQL | MongoDB             | MongoDB Atlas  |
| Cache (NoSQL) | Redis          | Upstash Redis  |

## Como rodar

### 1. Criar contas gratuitas

- **Supabase** (PostgreSQL): https://supabase.com
  - Crie um projeto → copie a URL e Anon Key
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
| POST   | `/api/users` | Criar/login de usuário |
| GET    | `/api/users` | Listar todos os usuários |
| GET    | `/api/users/{id}` | Detalhes de um usuário |
| POST   | `/api/users/{id}/hobbies` | Adicionar hobby |
| GET    | `/api/users/{id}/hobbies` | Listar hobbies (com cache) |
| GET    | `/api/users/{id}/hobbies/{hobby_id}` | Detalhe de um hobby |
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

O ponto principal é que **cada hobby pode ter campos completamente diferentes** — isso é possível graças ao MongoDB ser schemaless.
