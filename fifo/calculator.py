"""
fifo/calculator.py — Calculadora FIFO Simples
"""

import pandas as pd
from datetime import datetime
import config


class FIFOCalculator:
    """
    Gerencia posições e calcula vendas via FIFO (First In, First Out).
    """
    
    def __init__(self):
        """Inicializa com carteira vazia ou carrega de arquivo se existir."""
        
        self.posicoes = {}  # {ticker: [lotes]}
        self.vendas_realizadas = []
        
        # Tenta carregar carteira existente
        if config.CARTEIRA_CSV.exists():
            self._carregar_carteira()
    
    def _carregar_carteira(self):
        """Carrega carteira_atual.csv."""
        try:
            df = pd.read_csv(config.CARTEIRA_CSV)
            for _, row in df.iterrows():
                ticker = row['ticker']
                if ticker not in self.posicoes:
                    self.posicoes[ticker] = []
                
                # Reconstrói lotes (simplificado — um lote com toda a posição)
                self.posicoes[ticker].append({
                    'quantidade': row['quantidade_atual'],
                    'custo_unitario': row['preco_medio_fifo'],
                    'mercado': row['mercado'],
                    'moeda': row['moeda'],
                    'corretora': row['corretora'],
                })
        except:
            pass
    
    def processar_operacoes(self, operacoes):
        """
        Processa lista de operações (compras/vendas) e atualiza posições.
        
        Args:
            operacoes: list de dicts
        
        Returns:
            vendas_realizadas: list de dicts com lucro/prejuízo
        """
        
        vendas = []
        
        for op in operacoes:
            tipo = op.get('tipo_operacao')
            
            if tipo == config.TIPO_COMPRA:
                self._processar_compra(op)
            
            elif tipo == config.TIPO_VENDA:
                venda_info = self._processar_venda(op)
                if venda_info:
                    vendas.append(venda_info)
            
            # TIPO_DIVIDENDO não afeta posições
        
        return vendas
    
    def _processar_compra(self, op):
        """Adiciona lote de compra à posição."""
        
        ticker = op['ticker']
        
        if ticker not in self.posicoes:
            self.posicoes[ticker] = []
        
        # Calcula custo unitário incluindo taxas rateadas
        custo_unitario = (
            op.get('custo_total_operacao', 0) / op.get('quantidade', 1)
        )
        
        lote = {
            'data': op.get('data_operacao'),
            'quantidade': op.get('quantidade', 0),
            'custo_unitario': custo_unitario,
            'mercado': op.get('mercado'),
            'moeda': op.get('moeda'),
            'corretora': op.get('corretora'),
        }
        
        self.posicoes[ticker].append(lote)
    
    def _processar_venda(self, op):
        """
        Consome lotes FIFO e calcula lucro/prejuízo.
        
        Returns:
            dict com info da venda realizada
        """
        
        ticker = op['ticker']
        quantidade_a_vender = op.get('quantidade', 0)
        
        if ticker not in self.posicoes or not self.posicoes[ticker]:
            # Venda sem compra anterior — erro, mas permite
            return {
                'id_venda': f"VENDA-{ticker}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'data_venda': op.get('data_operacao'),
                'ticker': ticker,
                'quantidade_vendida': quantidade_a_vender,
                'preco_venda_unitario': op.get('preco_unitario', 0),
                'valor_bruto_venda': op.get('valor_bruto', 0),
                'custo_fifo_da_venda': 0.0,
                'taxas_rateadas_venda': (
                    op.get('corretagem_rateada', 0) +
                    op.get('taxas_rateadas', 0) +
                    op.get('emolumentos_rateados', 0) +
                    op.get('impostos_rateados', 0)
                ),
                'lucro_prejuizo_realizado': op.get('custo_total_operacao', 0),  # Venda líquida
                'moeda': op.get('moeda'),
                'corretora': op.get('corretora'),
                'nome_arquivo': op.get('nome_arquivo'),
            }
        
        # Consome lotes FIFO
        custo_fifo_total = 0.0
        quantidade_restante = quantidade_a_vender
        
        while quantidade_restante > 0 and self.posicoes[ticker]:
            lote = self.posicoes[ticker][0]  # Primeiro lote (FIFO)
            
            if lote['quantidade'] <= quantidade_restante:
                # Consome lote inteiro
                custo_fifo_total += lote['quantidade'] * lote['custo_unitario']
                quantidade_restante -= lote['quantidade']
                self.posicoes[ticker].pop(0)
            else:
                # Consome parte do lote
                custo_fifo_total += quantidade_restante * lote['custo_unitario']
                lote['quantidade'] -= quantidade_restante
                quantidade_restante = 0
        
        # Calcula lucro/prejuízo
        valor_liquido_venda = op.get('custo_total_operacao', 0)  # Já tem taxas subtraídas
        lucro_prejuizo = valor_liquido_venda - custo_fifo_total
        
        return {
            'id_venda': f"VENDA-{ticker}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'data_venda': op.get('data_operacao'),
            'ticker': ticker,
            'quantidade_vendida': quantidade_a_vender,
            'preco_venda_unitario': op.get('preco_unitario', 0),
            'valor_bruto_venda': op.get('valor_bruto', 0),
            'custo_fifo_da_venda': custo_fifo_total,
            'taxas_rateadas_venda': (
                op.get('corretagem_rateada', 0) +
                op.get('taxas_rateadas', 0) +
                op.get('emolumentos_rateadas', 0) +
                op.get('impostos_rateados', 0)
            ),
            'lucro_prejuizo_realizado': lucro_prejuizo,
            'moeda': op.get('moeda'),
            'corretora': op.get('corretora'),
            'nome_arquivo': op.get('nome_arquivo'),
        }
    
    def get_carteira_atual(self):
        """
        Retorna snapshot da carteira atual.
        
        Returns:
            list de dicts (formato config.COLUNAS_CARTEIRA)
        """
        
        carteira = []
        
        for ticker, lotes in self.posicoes.items():
            if not lotes:
                continue
            
            # Soma todos os lotes do ticker
            quantidade_total = sum(l['quantidade'] for l in lotes)
            custo_total = sum(l['quantidade'] * l['custo_unitario'] for l in lotes)
            preco_medio = custo_total / quantidade_total if quantidade_total > 0 else 0
            
            # Pega mercado/moeda do primeiro lote
            primeiro_lote = lotes[0]
            
            carteira.append({
                'ticker': ticker,
                'mercado': primeiro_lote.get('mercado'),
                'moeda': primeiro_lote.get('moeda'),
                'quantidade_atual': quantidade_total,
                'custo_total_aberto': custo_total,
                'preco_medio_fifo': preco_medio,
                'corretora': primeiro_lote.get('corretora'),
                'data_atualizacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        return carteira
