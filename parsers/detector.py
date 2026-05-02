"""
parsers/detector.py — Detecta Corretora e Mercado Automaticamente
"""

import config


def detect_broker_and_market(content, filename):
    """
    Identifica corretora e mercado baseado em palavras-chave.
    
    Args:
        content: str (texto do PDF) ou DataFrame (CSV/Excel)
        filename: nome do arquivo
    
    Returns:
        dict: {
            'broker': 'schwab' | 'tdameritrade' | 'rico' | 'xp' | 'clear' | None,
            'market': 'USA' | 'B3' | None,
            'confidence': float (0.0-1.0),
        }
    """
    
    # Converte DataFrame para texto se necessário
    if hasattr(content, 'to_string'):
        text = content.to_string()
    else:
        text = str(content)
    
    # Junta filename + texto para busca
    search_text = (filename + " " + text).lower()
    
    # Detecta corretora
    broker = None
    max_matches = 0
    
    for broker_id, keywords in config.BROKER_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw.lower() in search_text)
        if matches > max_matches:
            max_matches = matches
            broker = broker_id
    
    # Detecta mercado baseado na corretora
    if broker in ['schwab', 'tdameritrade']:
        market = config.MERCADO_USA
    elif broker in ['rico', 'xp', 'clear']:
        market = config.MERCADO_B3
    else:
        market = None
    
    # Calcula confiança (simples: % de keywords encontradas)
    if broker:
        total_keywords = len(config.BROKER_KEYWORDS[broker])
        confidence = max_matches / total_keywords if total_keywords > 0 else 0.0
    else:
        confidence = 0.0
    
    return {
        'broker': broker,
        'market': market,
        'confidence': confidence,
    }
