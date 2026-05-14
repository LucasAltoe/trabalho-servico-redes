# Sistema de Cadastro de Usuários e Perfis

**Disciplina:** Serviços de Redes para Internet  
**Grupo:** 1  
**Tema:** Sistema de Cadastro de Usuários e Perfis  

---

## Integrantes

- Lucas Guimarães Bosio Altoé — Matrícula: 20241si016
- Lorenzo Rainha Gomes — Matrícula: 20241si011
- Miguel Arcanjo Miranda Bello — Matrícula: 20241si023
- Fábio Augusto Souza Santos — Matrícula: 20241si008

---

## Descrição

Aplicação web conteinerizada com:

- **NGINX** — proxy reverso + frontend estático
- **FastAPI** — API REST com CRUD de usuários e perfis
- **PostgreSQL** — banco de dados com persistência em volume

---

## Topologia

```
Hospedeiro (navegador)
    │
    │  porta 80
    ▼
 [NGINX]  ──── /api/ ────►  [FastAPI :8080]
    │                              │
    │  serve /                     │
    ▼                              ▼
 html/css/js                  [PostgreSQL :5432]
                               (volume: dados-postgres)

Rede interna: netatividade01
```

---

## Estrutura do projeto

```
grupo1-usuarios/
├── docker-compose.yml       # Orquestra todos os serviços
├── .env                     # Variáveis de ambiente (não subir no Git)
├── .gitignore
├── README.md
├── backend/
│   ├── Dockerfile           # Imagem do backend Python/FastAPI
│   ├── requirements.txt     # Dependências Python
│   └── app/
│       ├── main.py          # Ponto de entrada da API
│       ├── database.py      # Conexão com o PostgreSQL
│       ├── models.py        # Tabelas do banco (SQLAlchemy)
│       ├── routes/
│       │   ├── usuarios.py  # Rotas CRUD de usuários
│       │   └── perfis.py    # Rotas CRUD de perfis
│       └── schemas/
│           ├── usuario.py   # Validação de dados de usuário
│           └── perfil.py    # Validação de dados de perfil
└── nginx/
    ├── nginx.conf           # Configuração do proxy reverso
    └── html/
        ├── index.html       # Interface web
        ├── style.css        # Estilos
        └── script.js        # Lógica do frontend (chamadas à API)
```

---

## Como executar

### Pré-requisitos
- Docker instalado
- Docker Compose instalado

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/grupo1-usuarios.git
cd grupo1-usuarios

# 2. Ajuste a senha no arquivo .env (use a matrícula de um integrante)
# O arquivo .env já está configurado — apenas verifique

# 3. Suba todos os containers
docker compose up --build

# 4. Acesse no navegador
# Frontend:  http://localhost
# Docs API:  http://localhost/api/docs
```

### Para parar
```bash
docker compose down
```

### Para parar e apagar os dados do banco
```bash
docker compose down -v
```

---

## Endpoints da API

### Usuários
| Método | Rota                  | Descrição              |
|--------|-----------------------|------------------------|
| GET    | /api/usuarios/        | Lista todos os usuários |
| GET    | /api/usuarios/{id}    | Busca usuário por ID   |
| POST   | /api/usuarios/        | Cria novo usuário      |
| PUT    | /api/usuarios/{id}    | Atualiza usuário       |
| DELETE | /api/usuarios/{id}    | Remove usuário         |

### Perfis
| Método | Rota                 | Descrição             |
|--------|----------------------|-----------------------|
| GET    | /api/perfis/         | Lista todos os perfis |
| GET    | /api/perfis/{id}     | Busca perfil por ID   |
| POST   | /api/perfis/         | Cria novo perfil      |
| PUT    | /api/perfis/{id}     | Atualiza perfil       |
| DELETE | /api/perfis/{id}     | Remove perfil         |

---

## Exemplo de uso (curl)

```bash
# Criar um perfil
curl -X POST http://localhost/api/perfis/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Administrador", "descricao": "Acesso total"}'

# Criar um usuário
curl -X POST http://localhost/api/usuarios/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Maria Silva", "email": "maria@email.com", "senha": "123456", "perfil_id": 1}'

# Listar usuários
curl http://localhost/api/usuarios/
```
