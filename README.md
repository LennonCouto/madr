# 📚 MADR API — Meu Acervo Digital de Romances

API REST para gerenciamento de livros e seus autores, com autenticação de usuários. Projeto desenvolvido com foco em consolidar conceitos fundamentais de backend.

---

## 🚀 Objetivo

Construir uma API simples e funcional que permita:

- Gerenciar usuários (criação, autenticação e controle de acesso)
- Gerenciar livros
- Gerenciar autores (romancistas)
- Relacionar livros com seus respectivos autores

Tudo isso usando apenas fundamentos essenciais

---

## 🧠 Conceitos Aplicados

- Arquitetura em camadas (Router → Service → Repository)
- CRUD completo
- Autenticação com JWT
- Relacionamento entre entidades
- Validação de dados
- Boas práticas com FastAPI

---

## 🏗️ Estrutura do Projeto

```
app/
├── routers/
├── schemas/
├── services/
├── repositories/
├── models/
├── db/
├── core/
└── main.py
```


---

## 🔐 Autenticação

A API utiliza JWT para proteger rotas.

Fluxo:

1. Usuário se registra
2. Faz login
3. Recebe um token JWT
4. Usa o token para acessar rotas protegidas

---

## 📌 Funcionalidades

### 👤 Usuários (Implementando)

- Criar conta
- Login
- Atualizar dados
- Deletar conta
- Proteção de rotas com JWT

---

### 📚 Livros (Em construção)

- Criar livro
- Listar livros
- Atualizar livro
- Deletar livro

---

### ✍️ Autores / Romancistas (Em construção)

- Criar autor
- Listar autores
- Atualizar autor
- Deletar autor

---

## ⚙️ Tecnologias

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL (ou SQLite)
- Pydantic
- JWT


---

## ▶️ Como rodar o projeto

```
# Clone o repositório
git clone https://github.com/seu-usuario/madr-api.git

# Entre na pasta
cd madr-api

# Instale as dependências
poetry install

# Rode o projeto
poetry run uvicorn app.main:app --reload
```


## 📦 Gerenciamento de Dependências

Este projeto utiliza Poetry para gerenciamento de dependências e ambiente virtual.
