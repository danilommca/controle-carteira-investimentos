"""
parsers/rico_parser.py — Parser para Rico (B3 Brasil)
"""

import config


def parse(content):
    """
    Extrai operações de nota Rico.
    
    Returns:
        tuple: (operacoes, taxas_totais)
    """
    
    # TODO: Implementar parsing específico Rico
    # Por enquanto, retorna vazio — usuário adiciona depois
    
    operacoes = []
    taxas_totais = {
        'corretagem': 0.0,
        'taxas': 0.0,
        'emolumentos': 0.0,
        'impostos': 0.0,
    }
    
    return operacoes, taxas_totais
