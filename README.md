# ![SKATLAZ](./assets/2026-06-19%20113312.png)

# Skatlaz Server Multimedia AI 3.0

## Beta Version

**Skatlaz Server Multimedia AI 3.0** is an advanced AI orchestration platform built with Django that combines Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), AI Agents, Multimedia Processing, MCP Servers, Fine-Tuning Pipelines, Web Crawling, and Local/Cloud AI Providers into a unified environment.

Designed for AI specialists, researchers, developers, educators, enterprises, and multimedia creators, Skatlaz Server provides a modular architecture capable of integrating multiple AI workflows through MCP (Modular Cognitive Processor) servers.

---

# 🚀 Main Features

## Artificial Intelligence

* Multi-Provider LLM Support
* Ollama Integration
* Google Gemini Integration
* DeepSeek Code Integration
* DeepSeek Coder Support
* Qwen Coder Support
* Prompt Templates
* AI Agents
* Chat Sessions
* Conversation History

## Retrieval-Augmented Generation (RAG)

* Document Collections
* Semantic Search
* Vector Embeddings
* Sentence Transformers
* ChromaDB
* FAISS
* PDF Indexing
* DOCX Indexing
* JSON Indexing
* TXT Indexing

## Multimedia AI

### Image Generation

* Flux
* SDXL Turbo
* Image Z-Turbo
* Grok Image
* OpenAI Image

### Video Generation

* Wan Video
* Open-Sora
* CogVideoX
* Hunyuan Video
* Grok Video

### Audio Generation

* Bark TTS
* Coqui TTS
* RVC
* Demucs
* FFmpeg

### Multimedia Processing

* OCR
* Speech-to-Text (STT)
* Text-to-Speech (TTS)
* Audio Enhancement
* Video Enhancement
* Image Processing

---

# 🧠 MCP Servers Architecture

MCP stands for:

**Modular Cognitive Processor**

MCP Servers extend the capabilities of Skatlaz Server through specialized AI modules.

Each MCP can provide:

* AI Agents
* Prompt Templates
* RAG Collections
* Fine-Tuning Datasets
* Automation Pipelines
* API Integrations
* Knowledge Bases
* Multimedia Services

---

# 📦 Included MCP Servers

## GexProg MCP

Software Engineering and Development

Features:

* Code Generation
* Debugging
* Refactoring
* Architecture Analysis
* Documentation Generation
* DeepSeek Code Integration

---

## OpenStudio MCP

Multimedia Production Platform

Features:

* Image Processing
* Video Processing
* Audio Processing
* OCR
* TTS
* STT
* FFmpeg Workflows

---

## Office AI Worker MCP

Business Productivity

Features:

* PDF Processing
* Word Documents
* OCR
* Translation
* Dashboards
* Presentations
* Spreadsheet Analysis

---

## Studies MCP

Educational Environment

Features:

* Courses
* Learning Plans
* Quizzes
* Presentations
* Academic Research

---

## Entertainment MCP

Media and Entertainment

Features:

* Movies
* TV Shows
* Music
* Recommendations
* Reviews
* Summaries

---

## Music Producer MCP

Audio Production

Features:

* Stem Separation
* Audio Mastering
* DSP Processing
* AI Music Generation
* Sound Design

---

## Money MCP

Financial Intelligence

Features:

* Market Analysis
* Currency Conversion
* KPI Dashboards
* Business Intelligence
* Statistics

---

## SurfTask MCP

Web Intelligence

Features:

* Web Crawling
* Scraping
* Metadata Extraction
* Website Summaries
* Search Automation

---

## WorldSports MCP

Sports Intelligence

Features:

* Rankings
* Historical Results
* Analytics
* Live Monitoring
* Performance Metrics

---

## InfoToday MCP

Information Retrieval

Features:

* Search
* News
* Transportation
* Weather
* Maps
* Research

---

# 🔧 MCP Infrastructure

## MCP Registry

```text
/ai/registry/
```

Stores all MCP definitions and metadata.

---

## MCP Pipelines

```text
/ai/pipelines/
```

Contains execution pipelines used by agents and workflows.

---

## MCP Servers Folder

```text
mcp_servers/
```

Contains installed MCP packages.

---

## Windows Launcher

```text
start_all_mcp_servers_and_skatlaz_3_0.bat
```

Starts:

* Skatlaz Server
* MCP Servers
* Ollama
* DeepSeek Code
* Multimedia Services
* OpenStudio Services

Using a single command.

---

# 🏗 Client Interface

Default Client Pages:

```text
/ai/
/ai/client/
```

Features:

* AI Chat
* Agent Selection
* Pipeline Selection
* MCP Selection
* RAG Search
* Multimedia Tasks
* Prompt Management

---

# ⚙ Configuration Endpoints

## Configuration

```http
GET /ai/config/
```

Returns system configuration and available MCP modules.

---

## MCP Task Execution

```http
POST /ai/mcp-task/
```

Executes specialized MCP workflows.

Example:

```json
{
  "task_type": "code",
  "prompt": "Create a Django API",
  "language": "python",
  "target_os": "windows"
}
```

---

# 🌐 REST API Endpoints

## Chat

```http
POST /ai/chat/
```

Example:

```json
{
  "prompt": "Explain RAG",
  "agent_id": 1,
  "collection_id": 1
}
```

---

## Available Models

```http
GET /ai/models/list/
```

---

## RAG Search

```http
GET /ai/rag/search/?q=search_term&collection_id=1
```

---

## Index Source

```http
POST /ai/rag/index-source/
```

Example:

```json
{
  "source_id": 1
}
```

---

## Start WebDiver

```http
POST /ai/crawler/start/
```

Example:

```json
{
  "url": "https://example.com",
  "diver_type": "_text",
  "collection_id": 1
}
```

---

## Prepare Fine-Tuning

```http
POST /ai/finetune/prepare/
```

Example:

```json
{
  "job_id": 1
}
```

---

## Export to Ollama

```http
POST /ai/ollama/export/
```

Example:

```json
{
  "job_id": 1
}
```

---

# 🎓 Multimedia Training MCP

Skatlaz Server 3.0 includes a complete training workflow for multimedia AI projects.

Supported:

* JSONL Datasets
* Prompt Datasets
* Metadata Datasets
* Generated Artifacts
* RAG Index Creation
* LoRA Preparation
* QLoRA Preparation
* Ollama Export

---

# 📥 Quick Installation

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py skatlaz_seed_ai

python manage.py runserver
```

---

# 🔐 Administration

Open:

```text
http://127.0.0.1:8000/admin/
```

Manage:

* LLM Providers
* AI Agents
* Agent Categories
* Prompt Templates
* RAG Collections
* RAG Chunks
* Training Datasets
* Fine-Tuning Jobs
* WebDiver Tasks
* MCP Servers
* Analytics

---

# 🖥 Recommended Local Models

## Coding

* DeepSeek Code
* DeepSeek Coder
* Qwen Coder

## General Purpose

* Gemma
* Mistral
* Llama

## Multimedia

* Flux
* SDXL Turbo
* Open-Sora
* CogVideoX

---

# ⚠ Important Note

LoRA and QLoRA training should not be executed inside the Django web process.

The platform generates:

* Training Scripts
* Modelfiles
* Dataset Packages
* Export Configurations

Actual training should run on:

* Dedicated GPU Machines
* Worker Nodes
* Kubernetes Jobs
* Cloud GPU Services

---

# 📄 License

Open Source and Freeware.

Developed by:

**Skatlaz Digi-AI Works Finder**

GitHub:

[https://github.com/skatlaz](https://github.com/skatlaz)

---

# 🚀 Skatlaz Server Multimedia AI 3.0

**Create. Automate. Connect. Evolve.**

The complete AI platform for specialists, researchers, developers, educators, and multimedia creators.
