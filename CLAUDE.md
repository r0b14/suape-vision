# SUAPE Vision — Guia do desenvolvedor

## O que é este projeto

API REST Flask para monitoramento de navios no Porto de Suape. Tem dois componentes separados:
1. **Web API** (`app.py`) — roda na Vercel, dados de escala de navios
2. **Módulo de visão** (`suape/`) — roda localmente, OpenCV + Azure Custom Vision

## Setup

```bash
pip install -r requirements-dev.txt
cp .env.example .env   # preencher AZURE_PREDICTION_KEY e AZURE_PREDICTION_URL
python app.py          # servidor local em http://localhost:5000
```

## Estrutura relevante

- `app.py` — rotas Flask; dados em `DADOS` (lista em memória, sem banco)
- `templates/` — Jinja2; páginas `index`, `api`, `guia`, `webhook`
- `static/logo.png` — logo servida pelo Flask (não usar URL externa do GitHub)
- `suape/getContainers/main.py` — lê `AZURE_PREDICTION_KEY` do ambiente
- `suape/getContainers/video.py` — rastreador CSRT; vídeo em `video/video_fast_4.mov` (não versionado)

## Convenções

- HTML fica em `templates/`, nunca inline em routes Python
- Credenciais sempre via variáveis de ambiente (`.env`), nunca hardcoded
- Arquivos `.mov` e `.env` estão no `.gitignore`
- `requirements.txt` é apenas Flask (para Vercel); dependências de CV ficam em `requirements-dev.txt`

## Deploy

Push para `main` → Vercel faz deploy automático do `app.py`.
O módulo `suape/` não é executado no Vercel — é local apenas.

## Variáveis de ambiente

| Variável | Uso |
|---|---|
| `FLASK_DEBUG` | `true` para hot-reload local |
| `AZURE_PREDICTION_KEY` | Chave da API Azure Custom Vision |
| `AZURE_PREDICTION_URL` | Endpoint do projeto de detecção |
