import streamlit as st
from utils import ler_pdf, analisar_dna_cliente, analisar_edital_com_dna

# --- CONFIGURAÇÃO DO COCKPIT ---
st.set_page_config(page_title="Apollo Mission Control", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #1e2130; border-radius: 5px; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b; color: white; }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.title("🚀 Projeto Apollo: Controle de Missão")
st.markdown("**Status:** Sistema Operacional | **IA:** Gemini 2.5 Flash")

# --- PAINEL LATERAL ---
st.sidebar.header("📟 Painel de Comando")
opcao = st.sidebar.radio("Sistema:", ["1. Hangar (Configurar Agência)", "2. Lançamento (Analisar Missão)"])

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 API Key:", type="password")

if 'agencias' not in st.session_state:
    st.session_state['agencias'] = {} 

# ==================================================
# SISTEMA 1: HANGAR
# ==================================================
if opcao == "1. Hangar (Configurar Agência)":
    st.header("🛸 Hangar: Calibragem de DNA")
    
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome da Agência")
        nuances = st.text_area("Diretrizes da Base", height=150)
    with col2:
        arquivos = st.file_uploader("Documentação (PDF)", type="pdf", accept_multiple_files=True)

    if st.button("🛠️ Processar"):
        if api_key and nome and arquivos:
            with st.spinner("🔄 Calibrando sensores..."):
                texto = ""
                for arq in arquivos: texto += ler_pdf(arq) + "\n"
                dna = analisar_dna_cliente(api_key, texto, nuances)
                st.session_state['agencias'][nome] = dna
                st.success(f"Agência '{nome}' calibrada!")
                st.info(dna)
        else:
            st.error("⚠️ Preencha todos os dados do Hangar.")

# ==================================================
# SISTEMA 2: LANÇAMENTO
# ==================================================
elif opcao == "2. Lançamento (Analisar Missão)":
    st.header("🪐 Simulação de Lançamento")
    
    if not st.session_state['agencias']:
        st.warning("⚠️ Hangar vazio.")
        st.stop()
    
    agencia = st.selectbox("🚀 Selecionar Nave:", list(st.session_state['agencias'].keys()))
    edital = st.file_uploader("📜 Carregar Edital (PDF)", type="pdf")
    
    if st.button("🔴 INICIAR ANÁLISE"):
        if edital:
            with st.spinner("🛰️ Processando telemetria da missão..."):
                texto_edital = ler_pdf(edital)
                dna = st.session_state['agencias'][agencia]
                
                # Chama a IA
                resultado_bruto = analisar_edital_com_dna(api_key, texto_edital, dna)
                
                # --- CORTE EM 3 ESTÁGIOS ---
                # O código tenta dividir o texto usando os separadores que criamos
                try:
                    # Separa a Parte 1 (Impeditivos) do resto
                    partes_1_resto = resultado_bruto.split("|||SEP_CONSULTOR|||")
                    parte_impeditivos = partes_1_resto[0]
                    
                    # Separa o resto em Parte 2 (Consultor) e Parte 3 (Cliente)
                    partes_2_3 = partes_1_resto[1].split("|||SEP_CLIENTE|||")
                    parte_consultor = partes_2_3[0]
                    parte_cliente = partes_2_3[1]
                    
                except IndexError:
                    # Se a IA falhar na formatação, mostra tudo junto para não dar erro
                    parte_impeditivos = resultado_bruto
                    parte_consultor = "⚠️ Erro na formatação automática."
                    parte_cliente = "⚠️ Erro na formatação automática."

                st.markdown("---")
                st.success("✅ Análise Concluída! Visualize os relatórios abaixo:")
                
                # Cria as 3 ABAS na ordem desejada
                tab1, tab2, tab3 = st.tabs(["🛑 1. IMPEDITIVOS (Veredito)", "👷 2. CONSULTOR (Técnico)", "👔 3. CLIENTE (Resumo)"])
                
                with tab1:
                    st.error("⚠️ LEIA PRIMEIRO: ANÁLISE DE RISCOS FATAIS")
                    st.markdown(parte_impeditivos)
                
                with tab2:
                    st.info("Detalhes para montagem da proposta")
                    st.markdown(parte_consultor)
                    
                with tab3:
                    st.success("Texto pronto para enviar ao Diretor")
                    st.markdown(parte_cliente)
        else:
            st.error("⚠️ Edital não carregado.")
