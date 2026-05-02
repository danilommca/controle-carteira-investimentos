"""
app.py — Importador Visual de Notas de Corretagem

Streamlit app para importar, conferir e consolidar operações.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Imports locais
import config
from utils.file_reader import read_file
from parsers import detector, schwab_parser, rico_parser, xp_parser, clear_parser, td_ameritrade_parser
from utils.rateio import ratear_taxas
from fifo.calculator import FIFOCalculator
from utils.exporters import exportar_operacoes, exportar_carteira, exportar_vendas, exportar_arquivo_processado, get_download_buttons_data


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Importador de Notas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS Global
st.markdown("""
<style>
.main {background-color: #f5f5f5;}
.stButton>button {width: 100%; border-radius: 5px;}
.success-box {background: #d4edda; padding: 1rem; border-radius: 5px; margin: 1rem 0;}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ESTADO DA SESSÃO
# ═══════════════════════════════════════════════════════════════════════════════

if 'operacoes_extraidas' not in st.session_state:
    st.session_state.operacoes_extraidas = None

if 'file_info' not in st.session_state:
    st.session_state.file_info = None


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_parser(broker):
    """Retorna o parser apropriado para a corretora."""
    parsers_map = {
        'schwab': schwab_parser,
        'tdameritrade': td_ameritrade_parser,
        'rico': rico_parser,
        'xp': xp_parser,
        'clear': clear_parser,
    }
    return parsers_map.get(broker)


def processar_arquivo(uploaded_file):
    """Processa arquivo enviado: lê, detecta corretora, extrai operações."""
    
    # 1. Lê arquivo
    file_data = read_file(uploaded_file)
    
    # 2. Detecta corretora e mercado
    detection = detector.detect_broker_and_market(file_data['content'], file_data['filename'])
    
    # 3. Seleciona parser
    parser = get_parser(detection['broker'])
    
    if not parser:
        st.error(f"❌ Corretora não reconhecida: {detection['broker']}")
        return None, None
    
    # 4. Extrai operações
    try:
        operacoes, taxas_totais = parser.parse(file_data['content'])
    except Exception as e:
        st.error(f"❌ Erro ao processar arquivo: {str(e)}")
        return None, None
    
    if not operacoes:
        st.warning("⚠️ Nenhuma operação encontrada no arquivo.")
        return None, None
    
    # 5. Rateia taxas
    operacoes = ratear_taxas(operacoes, taxas_totais)
    
    # 6. Adiciona campos extras
    for op in operacoes:
        op['nome_arquivo'] = file_data['filename']
        op['data_importacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        op['id_operacao'] = f"{op['ticker']}-{op['data_operacao'].strftime('%Y%m%d')}-{hash(str(op)) % 100000}"
        op['irrf'] = op.get('irrf', 0.0)
        op['dividendos'] = op.get('dividendos', 0.0) if op.get('tipo_operacao') == config.TIPO_DIVIDENDO else 0.0
    
    # Salva info do arquivo
    file_info = {
        'filename': file_data['filename'],
        'hash': file_data['hash'],
        'broker': detection['broker'],
        'market': detection['market'],
        'raw_bytes': file_data['raw_bytes'],
        'type': file_data['type'],
    }
    
    return operacoes, file_info


# ═══════════════════════════════════════════════════════════════════════════════
# INTERFACE PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

st.title("📊 Importador de Notas de Corretagem")
st.markdown("**Importe, confira e consolide suas operações — Brasil e EUA**")
st.markdown("---")

# Upload
uploaded_file = st.file_uploader(
    "📁 Envie sua nota de corretagem ou extrato",
    type=config.SUPPORTED_TYPES,
    help="Formatos suportados: PDF, CSV, XLSX, XLS"
)

if uploaded_file:
    
    # Processa apenas se for novo upload
    if st.session_state.file_info is None or st.session_state.file_info['filename'] != uploaded_file.name:
        
        with st.spinner("🔄 Processando arquivo..."):
            operacoes, file_info = processar_arquivo(uploaded_file)
            
            if operacoes:
                st.session_state.operacoes_extraidas = operacoes
                st.session_state.file_info = file_info
                st.success(f"✅ {len(operacoes)} operação(ões) extraída(s) de **{file_info['broker'].upper()}** ({file_info['market']})")
    
    # Se tem operações extraídas, mostra tela de conferência
    if st.session_state.operacoes_extraidas:
        
        st.markdown("---")
        st.subheader("🔍 Conferência Visual")
        
        # TELA DIVIDIDA
        col_left, col_right = st.columns([1, 1])
        
        # ─── LADO ESQUERDO: Arquivo Original ─────────────────────────────────
        with col_left:
            st.markdown("### 📄 Arquivo Original")
            
            file_info = st.session_state.file_info
            
            if file_info['type'] == 'pdf':
                # Mostra PDF
                st.markdown(f"**{file_info['filename']}**")
                st.markdown("*Preview de PDF disponível apenas em alguns navegadores*")
                
                # Download do PDF
                st.download_button(
                    "⬇ Baixar PDF",
                    data=file_info['raw_bytes'],
                    file_name=file_info['filename'],
                    mime="application/pdf"
                )
            
            else:
                # Mostra preview de CSV/Excel
                st.markdown(f"**{file_info['filename']}**")
                st.markdown("*Preview do arquivo:*")
                # TODO: Mostrar DataFrame preview
                st.info("Preview de CSV/Excel em desenvolvimento")
        
        # ─── LADO DIREITO: Dados Extraídos (Editável) ────────────────────────
        with col_right:
            st.markdown("### ✏️ Dados Extraídos (Editável)")
            
            # Converte para DataFrame
            df_ops = pd.DataFrame(st.session_state.operacoes_extraidas)
            
            # Colunas para exibição/edição
            colunas_exibir = [
                'data_operacao', 'ticker', 'tipo_operacao', 'quantidade',
                'preco_unitario', 'valor_bruto', 'corretagem_rateada',
                'taxas_rateadas', 'emolumentos_rateados', 'irrf', 'moeda'
            ]
            
            # Filtra colunas existentes
            colunas_exibir = [c for c in colunas_exibir if c in df_ops.columns]
            
            # Tabela editável
            edited_df = st.data_editor(
                df_ops[colunas_exibir],
                use_container_width=True,
                num_rows="dynamic",  # Permite adicionar/remover
                hide_index=True,
            )
            
            st.info("💡 **Dica:** Clique duplo para editar qualquer valor")
        
        # ─── BOTÕES DE AÇÃO ───────────────────────────────────────────────────
        st.markdown("---")
        
        col_confirm, col_cancel, col_space = st.columns([2, 2, 6])
        
        with col_confirm:
            if st.button("✅ Confirmar Importação", type="primary", use_container_width=True):
                
                with st.spinner("💾 Salvando..."):
                    
                    # Mescla dados editados de volta
                    for col in edited_df.columns:
                        df_ops[col] = edited_df[col]
                    
                    operacoes_final = df_ops.to_dict('records')
                    
                    # 1. Exporta operações
                    exportar_operacoes(operacoes_final)
                    
                    # 2. Atualiza FIFO
                    fifo = FIFOCalculator()
                    vendas = fifo.processar_operacoes(operacoes_final)
                    carteira = fifo.get_carteira_atual()
                    
                    # 3. Exporta carteira e vendas
                    exportar_carteira(carteira)
                    if vendas:
                        exportar_vendas(vendas)
                    
                    # 4. Registra arquivo processado
                    exportar_arquivo_processado({
                        'nome_arquivo': file_info['filename'],
                        'corretora_identificada': file_info['broker'],
                        'mercado': file_info['market'],
                        'data_processamento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'status': 'CONFIRMADO',
                        'hash_arquivo': file_info['hash'],
                        'observacoes': f"{len(operacoes_final)} operações importadas",
                    })
                    
                    # Limpa estado
                    st.session_state.operacoes_extraidas = None
                    st.session_state.file_info = None
                    
                    st.success("✅ **Importação confirmada!**")
                    st.balloons()
                    
                    # Rerun para limpar
                    st.rerun()
        
        with col_cancel:
            if st.button("❌ Cancelar", use_container_width=True):
                st.session_state.operacoes_extraidas = None
                st.session_state.file_info = None
                st.rerun()

else:
    # Estado inicial — sem arquivo
    st.info("👆 Envie um arquivo para começar")

# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO DE EXPORTAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.subheader("📥 Exportar Dados")

# Verifica se há dados para exportar
has_data = any([
    config.OPERACOES_CSV.exists(),
    config.CARTEIRA_CSV.exists(),
    config.VENDAS_CSV.exists(),
])

if has_data:
    
    downloads = get_download_buttons_data()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Operações Confirmadas**")
        if 'operacoes_csv' in downloads:
            st.download_button("⬇ CSV", data=downloads['operacoes_csv'], file_name="operacoes_confirmadas.csv", mime="text/csv")
        if 'operacoes_xlsx' in downloads:
            st.download_button("⬇ Excel", data=downloads['operacoes_xlsx'], file_name="operacoes_confirmadas.xlsx", mime="application/vnd.ms-excel")
    
    with col2:
        st.markdown("**Carteira Atual**")
        if 'carteira_csv' in downloads:
            st.download_button("⬇ CSV", data=downloads['carteira_csv'], file_name="carteira_atual.csv", mime="text/csv")
        if 'carteira_xlsx' in downloads:
            st.download_button("⬇ Excel", data=downloads['carteira_xlsx'], file_name="carteira_atual.xlsx", mime="application/vnd.ms-excel")
    
    with col3:
        st.markdown("**Vendas Realizadas**")
        if 'vendas_csv' in downloads:
            st.download_button("⬇ CSV", data=downloads['vendas_csv'], file_name="vendas_realizadas_fifo.csv", mime="text/csv")
        if 'vendas_xlsx' in downloads:
            st.download_button("⬇ Excel", data=downloads['vendas_xlsx'], file_name="vendas_realizadas_fifo.xlsx", mime="application/vnd.ms-excel")

else:
    st.info("Nenhum dado para exportar ainda. Importe sua primeira nota!")

# ═══════════════════════════════════════════════════════════════════════════════
# VISUALIZAÇÃO DA CARTEIRA ATUAL
# ═══════════════════════════════════════════════════════════════════════════════

if config.CARTEIRA_CSV.exists():
    st.markdown("---")
    st.subheader("📊 Carteira Atual (FIFO)")
    
    df_carteira = pd.read_csv(config.CARTEIRA_CSV)
    
    # Métricas rápidas
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Total de Ativos", len(df_carteira))
    with col_b:
        total_custo = df_carteira['custo_total_aberto'].sum()
        st.metric("Custo Total", f"${total_custo:,.2f}")
    with col_c:
        ativos_b3 = len(df_carteira[df_carteira['mercado'] == 'B3'])
        st.metric("Ativos B3", ativos_b3)
    
    # Tabela
    st.dataframe(df_carteira, use_container_width=True, hide_index=True)

# Rodapé
st.markdown("---")
st.markdown("**Portfolio Importer** — Importador simples e funcional")
