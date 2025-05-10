# Webhook Event Processor  -  Realmate Challenge

## 🧠 Visão Geral

Este projeto é uma API RESTful desenvolvida com Django e Django REST Framework, projetada para processar eventos recebidos via webhooks relacionados a conversas e mensagens de atendimento (como chats de WhatsApp, Instagram ou portais de atendimento).
O sistema foi construído como parte de um desafio técnico com foco em boas práticas de desenvolvimento backend, modularidade e escalabilidade.

A API tem como objetivo receber eventos de forma desacoplada, registrá-los em um banco de dados relacional e fornecer endpoints para listar e consultar conversas junto com suas mensagens, de maneira paginada e documentada via Swagger/OpenAPI.

Ela segue princípios de Clean Architecture, separando responsabilidades em camadas de domínio, aplicação e infraestrutura, com uso de DTOs, serviços e factories para garantir uma base sólida e testável.

---

## 🧩 Funcionalidades

- Endpoint POST para processamento de webhooks recebidos
- Registro de conversas e mensagens no banco de dados
- Endpoint GET para listar conversas e mensagens paginadas
- Documentação automatizada com Swagger/OpenAPI
- Testes automatizados com pytest com cobertura mínima definida
- Comando customizado para geração de dados falsos para testes manuais (manage.py seed)
- Linting com ruff e cobertura com coverage

---

## 🚀 Tecnologias

- Python 3.13+
- Django 5.1
- Django Rest Framework
- DRF Spectacular (para documentação OpenAPI)
- Poetry (gerenciador de dependências)
- SQLite (default, pode ser substituído)

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone git@github.com:giovanivalente/webhook-event-processor.git
cd webhook-event-processor
```

### 2. Instale o Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Adicione o Poetry ao PATH (se necessário):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 3. Instale as dependências

```bash
poetry install
```

### 4. Ative o ambiente virtual

```bash
poetry shell
```

### 5. Aplique as migrações

```bash
python manage.py migrate
```

### 6. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

---

## 📮 Endpoints

### 1. `POST /webhook/`

Recebe eventos com o seguinte payload:

### Novo evento de conversa iniciada

```json
{
    "type": "NEW_CONVERSATION",
    "timestamp": "2025-02-21T10:20:41.349308",
    "data": {
        "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### Novo evento de mensagem recebida

```json
{
    "type": "NEW_MESSAGE",
    "timestamp": "2025-02-21T10:20:42.349308",
    "data": {
        "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
        "direction": "RECEIVED",
        "content": "Olá, tudo bem?",
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### Novo evento de mensagem enviada

```json
{
    "type": "NEW_MESSAGE",
    "timestamp": "2025-02-21T10:20:44.349308",
    "data": {
        "id": "16b63b04-60de-4257-b1a1-20a5154abc6d",
        "direction": "SENT",
        "content": "Tudo ótimo e você?",
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### Novo evento de conversa encerrada

```json
{
    "type": "CLOSE_CONVERSATION",
    "timestamp": "2025-02-21T10:20:45.349308",
    "data": {
        "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### Tipos suportados:

O campo `type` recebe as seguintes opções:

- `NEW_CONVERSATION`
- `NEW_MESSAGE`
- `CLOSE_CONVERSATION`

O campo `direction` recebe as seguintes opções:

- `RECEIVED`
- `SENT`


### 2. `GET /conversations/{id}/`

Retorna os dados de uma conversa específica com suas mensagens paginadas.

O endpoint recebe query params opcionais:

- `page_size`: quantidade de mensagens por página (ex: 10)
- `page`: número da página (ex: 1)

---

## 📘 Documentação da API

Este projeto utiliza drf-spectacular para gerar documentação automatizada da API no padrão OpenAPI 3.0.

```
http://localhost:8000/docs/
http://localhost:8000/redoc/
```
---

## ✅ Testes

Este projeto utiliza pytest para execução dos testes automatizados e coverage para geração de relatório de cobertura.

Para rodar os testes:

```bash
task test
```
O comando roda os testes e gera um relatório HTML que pode ser acessado em:

```
http://localhost:63342/webhook-event-processor/htmlcov/index.html
```

---

## 🗃️ População da Base de Dados

Este projeto inclui um comando de management para popular o banco com dados fictícios (útil para testes manuais e desenvolvimento local).

### Executar o comando de seed

```
python manage.py seed
```
Por padrão, será criada 1 conversa com 5 mensagens.

### Personalizar quantidade de dados

Você pode passar os argumentos --conversations e --messages:

```
python manage.py seed --conversations 3 --messages 10
```

Esse exemplo cria 3 conversas, cada uma com 10 mensagens.

---

## 🛠 Estrutura do Projeto

```
realmate_challenge
├── shared
└── webhook_api
    ├── contracts
    │   └── repositories
    ├── entities
    ├── management
    │   ├── commands
    ├── migrations
    ├── models
    ├── repositories
    ├── serializers
    ├── tests
    │   ├── integration_tests
    │   └── unit_tests
    │       ├── use_cases
    │       └── views
    ├── use_cases
    └── views
```

---

## 🧾 Licença

Este projeto é apenas para fins educacionais/desafio técnico.