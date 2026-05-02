"""
parsers/td_ameritrade_parser.py — Parser para TD Ameritrade
"""

import config


def parse(content):
    """Extrai operações de extrato TD Ameritrade."""
    
    # TODO: Implementar parsing específico TD Ameritrade
    
    operacoes = []
    taxas_totais = {
        'corretagem': 0.0,
        'taxas': 0.0,
        'emolumentos': 0.0,
        'impostos': 0.0,
    }
    
    return operacoes, taxas_totais
