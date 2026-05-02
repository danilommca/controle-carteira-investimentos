"""
parsers/xp_parser.py — Parser para XP (B3 Brasil)
"""

import config


def parse(content):
    """Extrai operações de nota XP."""
    
    # TODO: Implementar parsing específico XP
    
    operacoes = []
    taxas_totais = {
        'corretagem': 0.0,
        'taxas': 0.0,
        'emolumentos': 0.0,
        'impostos': 0.0,
    }
    
    return operacoes, taxas_totais
