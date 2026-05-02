"""
utils/exporters.py — Exportação CSV e Excel
"""

import pandas as pd
import config
from datetime import datetime


def exportar_operacoes(operacoes):
    """
    Salva operações em CSV e Excel.
    
    Args:
        operacoes: list de dicts
    """
    
    if not operacoes:
        return
    
    df = pd.DataFrame(operacoes)
    
    # Adiciona colunas faltantes se necessário
    for col in config.COLUNAS_OPERACOES:
        if col not in df.columns:
            df[col] = None
    
    # Reordena colunas
    df = df[config.COLUNAS_OPERACOES]
    
    # Salva CSV
    df.to_csv(config.OPERACOES_CSV, mode='a', header=not config.OPERACOES_CSV.exists(), index=False, encoding='utf-8-sig')
    
    # Salva Excel (sobrescreve sempre — ler CSV e salvar tudo)
    if config.OPERACOES_CSV.exists():
        df_full = pd.read_csv(config.OPERACOES_CSV)
    else:
        df_full = df
    
    df_full.to_excel(config.OPERACOES_XLSX, index=False, sheet_name='Operações')


def exportar_carteira(carteira):
    """
    Salva carteira atual em CSV e Excel.
    
    Args:
        carteira: list de dicts
    """
    
    if not carteira:
        return
    
    df = pd.DataFrame(carteira)
    
    # Garante colunas
    for col in config.COLUNAS_CARTEIRA:
        if col not in df.columns:
            df[col] = None
    
    df = df[config.COLUNAS_CARTEIRA]
    
    # Salva CSV (sobrescreve)
    df.to_csv(config.CARTEIRA_CSV, index=False, encoding='utf-8-sig')
    
    # Salva Excel
    df.to_excel(config.CARTEIRA_XLSX, index=False, sheet_name='Carteira Atual')


def exportar_vendas(vendas):
    """
    Salva vendas realizadas em CSV e Excel.
    
    Args:
        vendas: list de dicts
    """
    
    if not vendas:
        return
    
    df = pd.DataFrame(vendas)
    
    # Garante colunas
    for col in config.COLUNAS_VENDAS:
        if col not in df.columns:
            df[col] = None
    
    df = df[config.COLUNAS_VENDAS]
    
    # Salva CSV (append)
    df.to_csv(config.VENDAS_CSV, mode='a', header=not config.VENDAS_CSV.exists(), index=False, encoding='utf-8-sig')
    
    # Salva Excel (ler tudo e sobrescrever)
    if config.VENDAS_CSV.exists():
        df_full = pd.read_csv(config.VENDAS_CSV)
    else:
        df_full = df
    
    df_full.to_excel(config.VENDAS_XLSX, index=False, sheet_name='Vendas Realizadas')


def exportar_arquivo_processado(info_arquivo):
    """
    Registra arquivo processado em CSV e Excel.
    
    Args:
        info_arquivo: dict
    """
    
    df = pd.DataFrame([info_arquivo])
    
    # Garante colunas
    for col in config.COLUNAS_ARQUIVOS:
        if col not in df.columns:
            df[col] = None
    
    df = df[config.COLUNAS_ARQUIVOS]
    
    # Salva CSV (append)
    df.to_csv(config.ARQUIVOS_CSV, mode='a', header=not config.ARQUIVOS_CSV.exists(), index=False, encoding='utf-8-sig')
    
    # Salva Excel (ler tudo e sobrescrever)
    if config.ARQUIVOS_CSV.exists():
        df_full = pd.read_csv(config.ARQUIVOS_CSV)
    else:
        df_full = df
    
    df_full.to_excel(config.ARQUIVOS_XLSX, index=False, sheet_name='Arquivos Processados')


def get_download_buttons_data():
    """
    Retorna DataFrames para download direto no Streamlit.
    
    Returns:
        dict: {
            'operacoes_csv': bytes,
            'operacoes_xlsx': bytes,
            'carteira_csv': bytes,
            'carteira_xlsx': bytes,
            'vendas_csv': bytes,
            'vendas_xlsx': bytes,
        }
    """
    
    data = {}
    
    # Operações
    if config.OPERACOES_CSV.exists():
        with open(config.OPERACOES_CSV, 'rb') as f:
            data['operacoes_csv'] = f.read()
    
    if config.OPERACOES_XLSX.exists():
        with open(config.OPERACOES_XLSX, 'rb') as f:
            data['operacoes_xlsx'] = f.read()
    
    # Carteira
    if config.CARTEIRA_CSV.exists():
        with open(config.CARTEIRA_CSV, 'rb') as f:
            data['carteira_csv'] = f.read()
    
    if config.CARTEIRA_XLSX.exists():
        with open(config.CARTEIRA_XLSX, 'rb') as f:
            data['carteira_xlsx'] = f.read()
    
    # Vendas
    if config.VENDAS_CSV.exists():
        with open(config.VENDAS_CSV, 'rb') as f:
            data['vendas_csv'] = f.read()
    
    if config.VENDAS_XLSX.exists():
        with open(config.VENDAS_XLSX, 'rb') as f:
            data['vendas_xlsx'] = f.read()
    
    return data
