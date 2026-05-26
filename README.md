# SUAPE Vision

API REST e sistema de visão computacional para monitoramento de navios e contêineres no Porto de Suape (PE, Brasil).

**Acesse ao vivo:** [suapevision.vercel.app](https://suapevision.vercel.app)

---

## Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Dashboard web | Feed de câmera ao vivo (CAM-01) + tabela de dados por berço |
| API REST JSON | Consulta de navios com filtros por ID e data |
| Download CSV | Exportação dos dados de escala |
| Detecção de contêineres | Integração com Azure Custom Vision para detecção em imagens |
| Rastreamento em vídeo | Rastreamento de contêineres frame a frame com OpenCV (CSRT) |

---

## Tecnologias

- **Backend:** Python 3.11+, Flask
- **Deploy:** Vercel (`@vercel/python`)
- **Visão computacional:** OpenCV, Pillow, Azure Custom Vision
- **Frontend:** HTML/CSS (Jinja2 templates)

---

## Estrutura do projeto

```
suape-vision/
├── app.py                      # Aplicação Flask principal
├── requirements.txt            # Dependências de produção (Vercel)
├── requirements-dev.txt        # Dependências de desenvolvimento (visão computacional)
├── vercel.json                 # Configuração de deploy
├── .env.example                # Template de variáveis de ambiente
├── templates/
│   ├── index.html              # Dashboard principal
│   ├── api.html                # Página de boas-vindas da API
│   ├── guia.html               # Documentação interativa da API
│   └── webhook.html            # Configuração de webhook
├── static/
│   └── logo.png                # Logo SUAPE Vision
└── suape/                      # Módulo de visão computacional (local)
    ├── start.py                # Orquestrador dos processos
    ├── getContainers/
    │   ├── main.py             # Detecção via Azure Custom Vision
    │   └── video.py            # Rastreamento em vídeo com OpenCV
    └── images/
        └── images.py           # Visualizador de imagens em tempo real (tkinter)
```

---

## Configuração local

### 1. Clone o repositório

```bash
git clone https://github.com/r0b14/suape-vision.git
cd suape-vision
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

### 3. Instale as dependências

Para executar apenas a API web:
```bash
pip install -r requirements.txt
```

Para usar os módulos de visão computacional:
```bash
pip install -r requirements-dev.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite .env com suas credenciais Azure
```

### 5. Execute a aplicação

```bash
python app.py
```

Acesse em `http://localhost:5000`.

---

## API Reference

### `GET /api/dados`
Retorna todos os registros de navios.

```json
[
  {
    "id": "GH89J",
    "categoria": "Feeder Ship",
    "entrada": "0",
    "saida": "0",
    "dock": "A1",
    "data": "2024-04-20"
  }
]
```

### `GET /api/dados/id/<id>`
Filtra por ID do navio.

### `GET /api/dados/data/<data>`
Filtra por data (`YYYY-MM-DD`).

### `GET /api/dados/id/<id>/data/<data>`
Combinação dos dois filtros.

### `GET /download_csv`
Baixa os dados em formato CSV.

**Resposta de erro (404):**
```json
{ "erro": "Nenhum registro encontrado." }
```

---

## Módulo de visão computacional

O diretório `suape/` contém ferramentas locais independentes da API web.

### Detecção em imagens (Azure)

Requer as variáveis `AZURE_PREDICTION_KEY` e `AZURE_PREDICTION_URL` no `.env`.

```bash
cd suape
python getContainers/main.py
```

### Rastreamento em vídeo

Coloque o arquivo de vídeo em `suape/getContainers/video/` e execute:

```bash
cd suape
python getContainers/video.py
```

Pressione **Q** para encerrar.

### Iniciar todos os módulos juntos

```bash
cd suape
python start.py
```

---

## Deploy (Vercel)

O deploy é automático via integração com o GitHub. Qualquer push para `main` aciona um novo deploy.

Para configurar manualmente:
```bash
vercel --prod
```

---

## Licença

Desenvolvido para o Porto de Suape — Pernambuco, Brasil.
