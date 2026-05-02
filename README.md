# Portfolio Importer — Importador Visual de Notas

Sistema simples e funcional para importar notas de corretagem (Brasil e EUA) com conferência visual e FIFO básico.

## 🎯 Características

✅ **Upload visual** — Arraste arquivos direto no navegador
✅ **Detecção automática** — Identifica corretora e mercado
✅ **Conferência lado a lado** — PDF original vs dados extraídos
✅ **Edição manual** — Tabela editável antes de confirmar
✅ **Rateio proporcional** — Taxas distribuídas corretamente
✅ **FIFO básico** — Controle de lotes e vendas realizadas
✅ **Export CSV/Excel** — Operações, carteira, vendas

## 📦 Corretoras Suportadas

**Brasil (B3):**
- Rico
- XP Investimentos
- Clear

**EUA:**
- Charles Schwab (CSV implementado)
- TD Ameritrade

## 🚀 Como Usar

### 1. Instalar

```bash
pip install -r requirements.txt
```

### 2. Rodar

```bash
streamlit run app.py
```

### 3. Importar

1. Arraste sua nota (PDF/CSV/Excel)
2. Confira os dados extraídos
3. Edite se necessário
4. Confirme importação
5. Baixe CSV/Excel

## 📂 Arquivos Gerados

Todos em `data/exports/`:

- `operacoes_confirmadas.csv` / `.xlsx`
- `carteira_atual.csv` / `.xlsx`
- `vendas_realizadas_fifo.csv` / `.xlsx`
- `arquivos_processados.csv` / `.xlsx`

## 🔧 Estrutura

```
portfolio_importer/
├── app.py                      # Streamlit app
├── config.py                   # Configurações
├── parsers/                    # Parsers por corretora
│   ├── detector.py
│   ├── schwab_parser.py
│   └── ...
├── fifo/
│   └── calculator.py           # FIFO básico
├── utils/
│   ├── file_reader.py
│   ├── rateio.py
│   └── exporters.py
└── data/exports/               # Arquivos gerados
```

## ➕ Adicionar Novas Corretoras

1. Crie `parsers/nome_parser.py`
2. Implemente função `parse(content)` que retorna `(operacoes, taxas_totais)`
3. Adicione keywords em `config.BROKER_KEYWORDS`

## 📊 Campos Extraídos

- Data da operação
- Ticker / ativo
- Tipo (compra/venda/dividendo)
- Quantidade
- Preço unitário
- Valor bruto
- Corretagem rateada
- Taxas rateadas
- Emolumentos rateados
- IRRF
- Moeda (BRL/USD)
- Mercado (B3/USA)

## 🎓 FIFO

Cada compra cria um lote.
Cada venda consome lotes mais antigos primeiro.
Lucro/prejuízo calculado automaticamente.

## ⚠️ Limitações

- Parsers B3 (Rico, XP, Clear) são skeletons — precisam implementação
- PDF parsing simplificado — CSV funciona melhor
- Sem banco de dados — tudo em CSV/Excel
- Sem autenticação — uso local apenas

## 📝 Próximos Passos (se quiser evoluir)

1. Implementar parsers B3 completos
2. Melhorar preview de PDF (streamlit-pdf-viewer)
3. Adicionar gráficos de patrimônio
4. Adicionar cálculo de impostos
5. Migrar para banco SQLite

---

**Versão:** 1.0.0-simple  
**Status:** ✅ Funcional para Schwab CSV  
**Data:** 2026-05-01
