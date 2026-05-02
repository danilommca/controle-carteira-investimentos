"""
config.py — Configurações Simples do Importador
"""

from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════════════════════

ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
EXPORTS_DIR = DATA_DIR / "exports"

# Criar diretórios se não existirem
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Arquivos de exportação
OPERACOES_CSV = EXPORTS_DIR / "operacoes_confirmadas.csv"
OPERACOES_XLSX = EXPORTS_DIR / "operacoes_confirmadas.xlsx"
CARTEIRA_CSV = EXPORTS_DIR / "carteira_atual.csv"
CARTEIRA_XLSX = EXPORTS_DIR / "carteira_atual.xlsx"
VENDAS_CSV = EXPORTS_DIR / "vendas_realizadas_fifo.csv"
VENDAS_XLSX = EXPORTS_DIR / "vendas_realizadas_fifo.xlsx"
ARQUIVOS_CSV = EXPORTS_DIR / "arquivos_processados.csv"
ARQUIVOS_XLSX = EXPORTS_DIR / "arquivos_processados.xlsx"

# ═══════════════════════════════════════════════════════════════════════════════
# CORRETORAS SUPORTADAS
# ═══════════════════════════════════════════════════════════════════════════════

BROKERS = {
    'schwab': 'Charles Schwab',
    'tdameritrade': 'TD Ameritrade',
    'rico': 'Rico',
    'xp': 'XP Investimentos',
    'clear': 'Clear',
}

# Keywords para detecção de corretora
BROKER_KEYWORDS = {
    'schwab': ['charles schwab', 'schwab', 'schwab.com', 'brokerage account'],
    'tdameritrade': ['td ameritrade', 'ameritrade', 'thinkorswim', 'tdameritrade'],
    'rico': ['rico corretora', 'rico investimentos', 'rico ctvm'],
    'xp': ['xp investimentos', 'xp dtvm', 'xp corretora'],
    'clear': ['clear corretora', 'clear ctvm', 'clear investimentos'],
}

# ═══════════════════════════════════════════════════════════════════════════════
# TIPOS DE OPERAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════

TIPO_COMPRA = "COMPRA"
TIPO_VENDA = "VENDA"
TIPO_DIVIDENDO = "DIVIDENDO"

# ═══════════════════════════════════════════════════════════════════════════════
# MOEDAS E MERCADOS
# ═══════════════════════════════════════════════════════════════════════════════

MOEDA_BRL = "BRL"
MOEDA_USD = "USD"

MERCADO_B3 = "B3"
MERCADO_USA = "USA"

# ═══════════════════════════════════════════════════════════════════════════════
# COLUNAS DOS CSVs
# ═══════════════════════════════════════════════════════════════════════════════

COLUNAS_OPERACOES = [
    'id_operacao',
    'data_operacao',
    'corretora',
    'mercado',
    'ticker',
    'tipo_operacao',
    'quantidade',
    'preco_unitario',
    'valor_bruto',
    'corretagem_rateada',
    'taxas_rateadas',
    'emolumentos_rateados',
    'impostos_rateados',
    'irrf',
    'dividendos',
    'custo_total_operacao',
    'moeda',
    'nome_arquivo',
    'data_importacao',
]

COLUNAS_CARTEIRA = [
    'ticker',
    'mercado',
    'moeda',
    'quantidade_atual',
    'custo_total_aberto',
    'preco_medio_fifo',
    'corretora',
    'data_atualizacao',
]

COLUNAS_VENDAS = [
    'id_venda',
    'data_venda',
    'ticker',
    'quantidade_vendida',
    'preco_venda_unitario',
    'valor_bruto_venda',
    'custo_fifo_da_venda',
    'taxas_rateadas_venda',
    'lucro_prejuizo_realizado',
    'moeda',
    'corretora',
    'nome_arquivo',
]

COLUNAS_ARQUIVOS = [
    'nome_arquivo',
    'corretora_identificada',
    'mercado',
    'data_processamento',
    'status',
    'hash_arquivo',
    'observacoes',
]

# ═══════════════════════════════════════════════════════════════════════════════
# FORMATOS DE ARQUIVO SUPORTADOS
# ═══════════════════════════════════════════════════════════════════════════════

SUPPORTED_TYPES = ['pdf', 'csv', 'xlsx', 'xls']
