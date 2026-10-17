# Nexum AI Prompt Optimizer Agent

---
<div align="center">

![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Release](https://img.shields.io/badge/Release-v1.0.0-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

</div>


Um agente inteligente focado em **otimização, refinamento e estruturação de prompts**, construído com o **Google ADK (Agent Development Kit)** e potencializado pela API do Google GenAI. Ideal para engenharia de prompts em aplicações de **RAG (Retrieval-Augmented Generation)** e cenários onde o alinhamento de contexto e precisão do modelo são críticos.

---
## 🚀 Funcionalidades

* **Otimização Inteligente de Prompts**: Transforma prompts vagos, confusos ou mal estruturados em instruções claras, eficientes e otimizadas para LLMs.
* **Foco Especial em RAG**: Ajuda a estruturar delimitadores, diretrizes de contexto e tratamento de alucinações.
* **Gerenciamento de Sessão e Memória**: Utiliza `DatabaseSessionService` (SQLite/Async) e `InMemoryMemoryService` para manter o histórico e o estado das interações via ADK.
* **Pronto para Produção**: API REST desenvolvida em FastAPI, empacotada com suporte a Docker, Kubernetes/GKE e compatível com plataformas de agentes.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.14+**
* **Google ADK (`google-adk`)**
* **Google GenAI SDK (`google-genai`)**
* **FastAPI & Uvicorn**
* **Docker & Kubernetes / GKE**
* **Uv** (Gerenciador de pacotes e dependências)

---

## 📂 Estrutura do Projeto

```text
nexum-ai-prompt-optimizer-agent/
├── prompt_optimizer/
│   ├── __init__.py
│   ├── agent.py        # Definição do root_agent (Google ADK)
│   ├── api.py          # Aplicação FastAPI e rotas (/v1/optimize)
│   ├── models.py       # Modelos de requisição e resposta (Pydantic)
│   └── memory.db       # Banco de dados de sessão (SQLite)
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

## ⚙️ Como Executar Localmente
### Pré-requisitos
- Python 3.14+ instalado.
- O gerenciador de pacotes uv instalado (pip install uv).
- Uma chave de API da Google configurada no ambiente.

1. Configuração de Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto (ou dentro da pasta prompt_optimizer) com sua chave de API:

```shell
GEMINI_API_KEY=sua_chave_aqui
```
2. Instalação de Dependências e Execução
Execute os comandos abaixo para sincronizar as dependências e iniciar o servidor de desenvolvimento localmente via `api.py`:

```Bash
# Sincroniza as dependências usando o uv
uv sync

# Executa a API localmente
uv run python prompt_optimizer/api.py
```
A API estará acessível em `http://localhost:8080` (com documentação interativa em `/docs`).

## 🐳 Executando via Docker
Para empacotar e rodar a aplicação em um container isolado:

1. Build da Imagem
Na raiz do projeto (onde está o Dockerfile), execute:

```Bash
docker build -t nexum-ai-prompt-optimizer .
```
2. Executando o Container
Passe a sua chave de API diretamente na execução:

```Bash
docker run -d \
  -p 8000:8000 \
  -e GEMINI_API_KEY="sua_chave_aqui" \
  --name prompt-optimizer-app \
  nexum-ai-prompt-optimizer
```
Acesse a API em `http://localhost:8000/v1/optimize.`

## ☁️ Deploy em Produção (Kubernetes / GKE)
Este agente pode ser facilmente escalado em clusters Kubernetes (como o Google Kubernetes Engine - GKE).

1. Exemplo de Manifesto Kubernetes (`deployment.yaml`)
Crie um arquivo chamado `deployment.yaml`:

```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prompt-optimizer-deployment
  labels:
    app: prompt-optimizer
spec:
  replicas: 2
  selector:
    matchLabels:
      app: prompt-optimizer
  template:
    metadata:
      labels:
        app: prompt-optimizer
    spec:
      containers:
      - name: prompt-optimizer
        image: gcr.io/seu-projeto-gcp/nexum-ai-prompt-optimizer:latest
        ports:
        - containerPort: 8000
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: gemini-secret
              key: api-key
        resources:
          limits:
            cpu: "1"
            memory: "1Gi"
          requests:
            cpu: "500m"
            memory: "512Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: prompt-optimizer-service
spec:
  type: LoadBalancer
  selector:
    app: prompt-optimizer
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```
2. Aplicando no Cluster (GKE)
```Bash
# Autentique no seu cluster GKE
gcloud container clusters get-credentials <nome-do-cluster> --region=<sua-regiao> --project=<seu-projeto>

# Crie o Secret com sua chave
kubectl create secret generic gemini-secret --from-literal=api-key="sua_chave_aqui"

# Suba a aplicação
kubectl apply -f deployment.yaml
```
## 🌐 Integração com Agent Platform
Por ser construído utilizando o Google ADK, este agente expõe os padrões estruturais necessários para integração nativa com ecossistemas de Agent Platforms. A gestão de sessões baseada em async SQLite (DatabaseSessionService) e a interface padronizada de eventos do Runner garantem que o agente possa ser orquestrado, monitorado e consumido em larga escala por plataformas de agentes corporativas.

## 📄 Licença
Este projeto está sob a licença MIT.

---
(C) 2026 - Dioleti - www.dl.tec.br - Fabricio Paulo