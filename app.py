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
st.markdown("**Status:** Sistema Operacional | **IA:** Gemini 2.5 Flash (Modo Estratégico)")

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
    
    # Upload PRIMEIRO (Mudança de fluxo a pedido)
    st.info("Passo 1: Carregue os documentos da missão (Edital/TR)")
    edital = st.file_uploader("📜 Carregar Edital (PDF)", type="pdf")
    
    if not st.session_state['agencias']:
        st.warning("⚠️ Hangar vazio. Cadastre uma agência primeiro.")
        st.stop()
    
    # Seleção de Cliente DEPOIS
    if edital:
        st.info("Passo 2: Identifique a Agência para esta missão")
        agencia = st.selectbox("🚀 Selecionar Nave:", list(st.session_state['agencias'].keys()))
        
        if st.button("🔴 INICIAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("🛰️ Executando protocolo forense..."):
                texto_edital = ler_pdf(edital)
                dna = st.session_state['agencias'][agencia]
                
                # Chama a IA
                resultado_bruto = analisar_edital_com_dna(api_key, texto_edital, dna)
                
                # --- CORTE INTELIGENTE ---
                texto_limpo = resultado_bruto.replace("**|||SEP_CONSULTOR|||**", "|||SEP_CONSULTOR|||")
                texto_limpo = texto_limpo.replace("**|||SEP_CLIENTE|||**", "|||SEP_CLIENTE|||")
                
                # Tenta dividir
                try:
                    if "|||SEP_CONSULTOR|||" in texto_limpo:
                        temp = texto_limpo.split("|||SEP_CONSULTOR|||")
                        parte_1 = temp[0] # Alerta de Risco
                        resto = temp[1]
                        
                        if "|||SEP_CLIENTE|||" in resto:
                            temp2 = resto.split("|||SEP_CLIENTE|||")
                            parte_2 = temp2[0] # Análise Técnica
                            parte_3 = temp2[1] # Resumo Cliente
                        else:
                            parte_2 = resto
                            parte_3 = "⚠️ A IA não gerou o Resumo do Cliente separadamente."
                    else:
                        parte_1 = texto_limpo
                        parte_2 = "⚠️ Corte automático falhou."
                        parte_3 = "⚠️ Corte automático falhou."
                except Exception:
                    parte_1 = texto_limpo
                    parte_2 = "Erro."
                    parte_3 = "Erro."

                st.markdown("---")
                st.success("✅ Análise Forense Concluída!")
                
                # Cria as 3 ABAS com os nomes exatos do seu prompt
                tab1, tab2, tab3 = st.tabs(["🎯 1. ALERTA DE RISCO (Gaps)", "📊 2. ANÁLISE TÉCNICA (Consultor)", "📄 3. RESUMO EXECUTIVO (Cliente)"])
                
                with tab1:
                    st.error("⚠️ PONTOS CRÍTICOS E IMPUGNAÇÕES")
                    st.markdown(parte_1)
                
                with tab2:
                    st.info("ℹ️ DETALHAMENTO DO PROCESSO")
                    st.markdown(parte_2)
                    
                with tab3:
                    st.success("✉️ PRONTO PARA ENVIO")
                    st.markdown(parte_3)
