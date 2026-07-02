# Cluster Docker Swarm — Cadastro de Usuários e Perfis

**Disciplina:** Serviços de Redes para Internet
**Grupo:** 1 — **Orquestrador:** Docker Swarm
**Tema:** Sistema de Cadastro de Usuários e Perfis

---

## Integrantes

- Lucas Guimarães Bosio Altoé — Matrícula: 20241si016
- Lorenzo Rainha Gomes — Matrícula: 20241si011
- Miguel Arcanjo Miranda Bello — Matrícula: 20241si023
- Fábio Augusto Souza Santos — Matrícula: 20241si008

---

## Descrição

Evolução do Trabalho 01. A mesma aplicação (NGINX + FastAPI + PostgreSQL, com CRUD de
usuários e perfis) roda agora em um **cluster Docker Swarm com 2 VMs**, com separação de
camadas, coleta de logs no **Grafana Loki** e visualização no **Grafana** (extra).

---

## Topologia do cluster

```
        Seu computador (navegador)
                 │  porta 80 (site)   │ porta 3000 (Grafana)
                 ▼                    ▼
┌───────────────────────────────┐   ┌───────────────────────────────┐
│  VM2  —  camada = app         │   │  VM1  —  camada = dados        │
│  (manager do Swarm)           │   │  (worker do Swarm)             │
│                               │   │                               │
│  NGINX    (2 réplicas, :80)   │   │  PostgreSQL (1 réplica, volume)│
│  FastAPI  (2 réplicas)        │   │  Loki       (1 réplica, volume)│
│  Grafana  (1 réplica, :3000)  │   │                               │
└──────────────┬────────────────┘   └───────────────┬───────────────┘
               │                                     │
               └────────── rede overlay ─────────────┘
                        (rede-cluster)

Expostos ao host: NGINX (80) e Grafana (3000).
Só na rede interna (sem porta publicada): PostgreSQL, FastAPI e Loki.
```

### Onde cada serviço roda (placement constraints)

| Serviço    | VM (label)      | Réplicas | Porta exposta |
|------------|-----------------|----------|---------------|
| PostgreSQL | VM1 (`dados`)   | 1        | nenhuma       |
| Loki       | VM1 (`dados`)   | 1        | nenhuma       |
| NGINX      | VM2 (`app`)     | 2        | 80            |
| FastAPI    | VM2 (`app`)     | 2        | nenhuma       |
| Grafana    | VM2 (`app`)     | 1        | 3000          |

---

## Estrutura do projeto

```
trabalho-servico-redes/
├── docker-stack.yml          # Stack do Swarm (os 5 serviços)
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py           # + log de início, middleware de requisições, log de erro do banco
│       ├── database.py       # + lê a senha do secret do Swarm
│       ├── logger.py         # NOVO: envia logs para o Loki
│       ├── models.py, routes/, schemas/
├── nginx/
│   ├── nginx.conf            # proxy reverso + frontend estático
│   └── html/                 # index.html, style.css, script.js
├── loki/
│   └── loki-config.yaml      # configuração do Loki
└── grafana/
    └── datasource.yaml       # cadastra o Loki no Grafana automaticamente
```

---

## Como executar (passo a passo)

> Você vai criar 2 VMs com **Multipass**, montar o cluster Swarm e implantar a stack.
> Rode os comandos na ordem. Onde aparece `<IP-VM2>` ou `<IP-VM1>`, troque pelo IP real.

### Pré-requisitos (no seu computador)

- **Multipass** instalado — https://multipass.run (`sudo snap install multipass` no Ubuntu).

### 1. Criar as duas VMs

```bash
multipass launch --name vm1 --cpus 1 --memory 1G --disk 5G 22.04
multipass launch --name vm2 --cpus 2 --memory 2G --disk 8G 22.04
```

Veja os IPs (anote os dois):

```bash
multipass list
```

### 2. Montar o projeto dentro das duas VMs

O mesmo diretório do projeto precisa existir nas duas VMs (o bind mount procura o arquivo
no nó onde o container roda). O `mount` do Multipass resolve isso sem precisar de Git.
**Rode estes comandos de dentro da pasta do projeto** (`trabalho-servico-redes`):

```bash
multipass mount .  vm1:/home/ubuntu/projeto
multipass mount .  vm2:/home/ubuntu/projeto
```

### 3. Instalar o Docker nas duas VMs

Repita para `vm1` e para `vm2`:

```bash
multipass shell vm1
# --- dentro da VM ---
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
exit
```

```bash
multipass shell vm2
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
exit
```

> Saia (`exit`) e entre de novo na VM para o grupo `docker` valer sem `sudo`.

### 4. Iniciar o Swarm

Na **VM2** (que será o manager):

```bash
multipass shell vm2
docker swarm init --advertise-addr <IP-VM2>
```

Esse comando imprime um `docker swarm join --token ...`. **Copie a linha inteira.**

Na **VM1** (worker), cole o comando copiado:

```bash
multipass shell vm1
docker swarm join --token <TOKEN> <IP-VM2>:2377
```

Confira na VM2 que os dois nós apareceram:

```bash
docker node ls
```

### 5. Rotular os nós (separação de camadas)

Na **VM2** (manager):

```bash
docker node update --label-add camada=app   vm2
docker node update --label-add camada=dados vm1
```

### 6. Criar o secret da senha do banco

Na **VM2**. Use, por exemplo, a matrícula de um integrante:

```bash
printf "20241si016" | docker secret create db_password -
```

### 7. Buildar a imagem do FastAPI (na VM2)

O FastAPI é o único serviço com imagem própria, e ele roda na VM2, então basta buildar lá:

```bash
cd /home/ubuntu/projeto
docker build -t grupo1-fastapi:latest ./backend
```

### 8. Implantar a stack

Na **VM2**, dentro de `/home/ubuntu/projeto`:

```bash
docker stack deploy --resolve-image never -c docker-stack.yml grupo1
```

> `--resolve-image never` faz o Swarm usar a imagem local do FastAPI em vez de procurá-la
> em um registry. As imagens oficiais (postgres, nginx, loki, grafana) são baixadas por
> cada nó automaticamente.

---

## Verificar o estado

Na **VM2** (manager):

```bash
docker service ls          # os 5 serviços e a contagem de réplicas (ex: 2/2)
docker stack ps grupo1     # em qual nó cada tarefa está rodando
docker node ls             # os 2 nós do cluster
```

Acesse no navegador do seu computador:

- **Site:**    `http://<IP-VM2>`
- **Grafana:** `http://<IP-VM2>:3000`  → menu *Explore* → fonte **Loki** → veja os logs.

---

## Consultar os logs no Loki (via API HTTP)

O Loki não tem porta exposta ao host (fica só na rede interna). Para consultá-lo pela API,
subimos um container temporário **dentro da rede do cluster**. Rode na **VM2**:

```bash
# Labels disponíveis
docker run --rm --network grupo1_rede-cluster curlimages/curl \
  curl -s http://loki:3100/loki/api/v1/labels

# Logs do serviço fastapi nos últimos 10 minutos
docker run --rm --network grupo1_rede-cluster curlimages/curl \
  curl -sG 'http://loki:3100/loki/api/v1/query_range' \
  --data-urlencode 'query={service="fastapi"}' \
  --data-urlencode "start=$(date -d '10 minutes ago' +%s000000000)" \
  --data-urlencode "end=$(date +%s000000000)"
```

## Provar que os serviços de dados NÃO estão expostos

No seu computador (fora do cluster), tente acessar as portas internas — devem **falhar**:

```bash
curl http://<IP-VM1>:5432    # PostgreSQL — recusado (sem porta publicada)
curl http://<IP-VM1>:3100    # Loki       — recusado (sem porta publicada)
```

Isso demonstra que Postgres e Loki só são acessíveis por dentro da rede overlay.

---

## Encerrar

```bash
# Remover a stack (na VM2)
docker stack rm grupo1

# Apagar as VMs (no seu computador)
multipass delete vm1 vm2
multipass purge
```

---

## Logs enviados ao Loki

O FastAPI (`backend/app/logger.py`) envia ao Loki:

- **Inicialização** da aplicação.
- **Cada requisição** recebida (método, rota e código de resposta).
- **Erros de conexão** com o PostgreSQL.

---

## Desafio extra implementado

- **Grafana** (`grafana/grafana:latest`, porta 3000) na VM2, com o Loki já cadastrado como
  fonte de dados, para visualizar os logs pela interface web.
