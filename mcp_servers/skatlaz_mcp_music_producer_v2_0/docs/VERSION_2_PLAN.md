# Skatlaz MCP Music Producer 2.0

## Objetivo
Transformar a v1.1 em um produtor musical por prompt para o Buskplay AI-DSP Press e Skatlaz Server AI.

## Núcleo estável
- análise de áudio
- separação de stems com Demucs
- masterização com FFmpeg
- relatório por faixa
- ZIP final
- servidor FastAPI base

## Novos módulos 2.0
- Prompt Producer: interpreta pedidos como “adicione chuva, violinos e backing vocals”
- Arrangement Planner: gera plano de arranjo JSON/Markdown por faixa
- MusicGen Adapter opcional: gera camadas de áudio quando AudioCraft estiver instalado
- Presets de atmosfera:
  - Pink Floyd Blues
  - Great Gig Color
  - Busk Blues Book
  - Rain & Birds
  - Hammond + Strings

## Estratégia Windows
AudioCraft e MusicGen ficam opcionais. A v2 roda mesmo sem eles, gerando planos e mantendo masterização/stems.
