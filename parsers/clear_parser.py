"""
parsers/clear_parser.py — Parser para Clear (B3 Brasil)
"""

import config


def parse(content):
    """Extrai operações de nota Clear."""
    
    # TODO: Implementar parsing específico Clear
    
    operacoes = []
    taxas_totais = {
        'corretagem': 0.0,
        'taxas': 0.0,
        'emolumentos': 0.0,
        'impostos': 0.0,
    }
    
    return operacoes, taxas_totais
