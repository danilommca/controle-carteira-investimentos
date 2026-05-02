"""
parsers/schwab_parser.py — Parser para Charles Schwab
"""

import re
import pandas as pd
from datetime import datetime
import config


def parse(content):
    """
    Extrai operações de arquivo Schwab (CSV ou texto de PDF).
    
    Args:
        content: str ou DataFrame
    
    Returns:
        tuple: (operacoes, taxas_totais)
        
        operacoes: list de dicts com estrutura:
            {
                'data_operacao': datetime,
                'ticker': str,
                'tipo_operacao': 'COMPRA' | 'VENDA' | 'DIVIDENDO',
                'quantidade': float,
                'preco_unitario': float,
                'valor_bruto': float,
                'moeda': 'USD',
                'mercado': 'USA',
                'corretora': 'schwab',
            }
        
        taxas_totais: dict {
            'corretagem': float,
            'taxas': float,
            'emolumentos': float,
            'impostos': float,
        }
    """
    
    if isinstance(content, pd.DataFrame):
        return _parse_csv(content)
    else:
        return _parse_pdf_text(content)


def _parse_csv(df):
    """
    Parse Schwab CSV format.
    
    Formato típico Schwab:
    Date, Action, Symbol, Description, Quantity, Price, Fees & Comm, Amount
    """
    
    operacoes = []
    total_fees = 0.0
    
    # Normaliza nomes de colunas
    df.columns = [c.strip().lower() for c in df.columns]
    
    for idx, row in df.iterrows():
        # Skip linhas vazias ou headers repetidos
        if pd.isna(row.get('date')) or pd.isna(row.get('action')):
            continue
        
        action = str(row.get('action', '')).lower()
        
        # Identifica tipo de operação
        if 'buy' in action or 'bought' in action:
            tipo = config.TIPO_COMPRA
        elif 'sell' in action or 'sold' in action:
            tipo = config.TIPO_VENDA
        elif 'dividend' in action or 'div' in action:
            tipo = config.TIPO_DIVIDENDO
        else:
            continue  # Skip outras ações
        
        # Extrai dados
        try:
            data_str = str(row.get('date', ''))
            data_operacao = pd.to_datetime(data_str).to_pydatetime()
        except:
            continue
        
        ticker = str(row.get('symbol', row.get('ticker', ''))).strip()
        if not ticker or ticker == 'nan':
            continue
        
        quantidade = float(row.get('quantity', row.get('qty', 0)))
        preco = float(row.get('price', 0))
        amount = float(row.get('amount', 0))
        fees = float(row.get('fees & comm', row.get('fees', row.get('commission', 0))))
        
        # Para dividendos, quantidade é 0 e valor_bruto é o amount
        if tipo == config.TIPO_DIVIDENDO:
            valor_bruto = abs(amount)
            quantidade = 0
            preco = 0
        else:
            valor_bruto = abs(quantidade * preco)
        
        total_fees += abs(fees)
        
        operacoes.append({
            'data_operacao': data_operacao,
            'ticker': ticker,
            'tipo_operacao': tipo,
            'quantidade': abs(quantidade),
            'preco_unitario': abs(preco),
            'valor_bruto': valor_bruto,
            'moeda': config.MOEDA_USD,
            'mercado': config.MERCADO_USA,
            'corretora': 'schwab',
        })
    
    # Taxas totais (Schwab geralmente só tem fees/commission)
    taxas_totais = {
        'corretagem': total_fees,
        'taxas': 0.0,
        'emolumentos': 0.0,
        'impostos': 0.0,
    }
    
    return operacoes, taxas_totais


def _parse_pdf_text(text):
    """
    Parse Schwab PDF text (simplificado).
    
    Retorna estrutura vazia por enquanto — usuário pode adicionar parsing de PDF depois.
    """
    
    # TODO: Implementar parsing de PDF Schwab se necessário
    # Por enquanto, retorna vazio e usuário usará CSV
    
    return [], {'corretagem': 0.0, 'taxas': 0.0, 'emolumentos': 0.0, 'impostos': 0.0}
