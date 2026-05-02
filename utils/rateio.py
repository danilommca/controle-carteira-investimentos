"""
utils/rateio.py — Rateio Proporcional de Taxas
"""


def ratear_taxas(operacoes, taxas_totais):
    """
    Distribui taxas proporcionalmente ao valor bruto de cada operação.
    
    Args:
        operacoes: list de dicts (operações extraídas)
        taxas_totais: dict {
            'corretagem': float,
            'taxas': float,
            'emolumentos': float,
            'impostos': float,
        }
    
    Returns:
        operacoes com campos *_rateada preenchidos e custo_total_operacao calculado
    """
    
    # Calcula valor bruto total
    total_bruto = sum(op.get('valor_bruto', 0) for op in operacoes)
    
    if total_bruto == 0:
        # Sem operações ou valores zerados — não rateia
        for op in operacoes:
            op['corretagem_rateada'] = 0.0
            op['taxas_rateadas'] = 0.0
            op['emolumentos_rateados'] = 0.0
            op['impostos_rateados'] = 0.0
            op['custo_total_operacao'] = op.get('valor_bruto', 0)
        return operacoes
    
    # Rateia proporcionalmente
    for op in operacoes:
        peso = op.get('valor_bruto', 0) / total_bruto
        
        op['corretagem_rateada'] = taxas_totais.get('corretagem', 0) * peso
        op['taxas_rateadas'] = taxas_totais.get('taxas', 0) * peso
        op['emolumentos_rateados'] = taxas_totais.get('emolumentos', 0) * peso
        op['impostos_rateados'] = taxas_totais.get('impostos', 0) * peso
        
        # Calcula custo total da operação
        if op.get('tipo_operacao') == 'COMPRA':
            # Compra: soma taxas
            op['custo_total_operacao'] = (
                op.get('valor_bruto', 0) +
                op['corretagem_rateada'] +
                op['taxas_rateadas'] +
                op['emolumentos_rateados'] +
                op['impostos_rateados']
            )
        else:
            # Venda ou Dividendo: subtrai taxas
            op['custo_total_operacao'] = (
                op.get('valor_bruto', 0) -
                op['corretagem_rateada'] -
                op['taxas_rateadas'] -
                op['emolumentos_rateados'] -
                op['impostos_rateados']
            )
    
    return operacoes
