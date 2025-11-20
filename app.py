import streamlit as st
import pandas as pd
from utils import ler_pdf, analisar_dna_cliente, analisar_edital_com_dna

# --- CONFIGURAÇÃO DO COCKPIT ---
st.set_page_config(page_title="Apollo Mission Control", page_icon="🚀", layout="wide")

# Estilo CSS para deixar o relatório bonito
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .veredicto-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #1e2130;
        border: 1px solid #4a4e69;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho Espacial
st.title("🚀 Projeto Apollo: Controle de Missão")
st.markdown("**Status:** Sistema Operacional | **IA:** Gemini 2.5 Flash (Consultor Ativado)")

# --- COMPUTADOR DE BORDO (Sidebar) ---
st.sidebar.header("📟 Painel de Comando")
opcao = st.sidebar.radio("Selecione o Sistema:", ["1. Hangar (Configurar Agência)", "2. Lançamento (Analisar Missão)"])

# Chave de Acesso
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Insira Chave de Acesso (API Key):", type="password")

# Memória da Nave
if 'agencias' not in st.session_state:
    st.session_state['agencias'] = {} 

# ==================================================
# SISTEMA 1: HANGAR (DNA DA EMPRESA)
# ==================================================
if opcao == "1. Hangar (Configurar Agência)":
    st.header("🛸 Hangar: Calibragem de DNA Corporativo")
    st.info("Cadastre a capacidade técnica. A IA irá gerar um perfil estritamente técnico.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_empresa = st.text_input("Nome da Agência (Empresa)")
        nuances = st.text_area("Diretrizes da Base (O que vocês fazem de melhor?)", 
            placeholder="Ex: Somos fortes em obras civis, mas não temos engenheiro mecânico. Terceirizamos ar-condicionado.",
            height=150)
            
    with col2:
        st.write("📂 **Documentação Comprobatória**")
        st.write("(Contratos Sociais, Atestados Técnicos)")
        arquivos = st.file_uploader("Carregar Arquivos de Sistema", type="pdf", accept_multiple_files=True)

    if st.button("🛠️ Processar Capacidade Técnica"):
        if not api_key:
            st.error("⚠️ Chave de Acesso não inserida nos propulsores!")
        elif not nome_empresa or not arquivos:
            st.warning("⚠️ Dados insuficientes para decolagem.")
        else:
            with st.spinner("🔄 Auditoria IA em andamento..."):
                # 1. Processar Documentos
                texto_total = ""
                for arq in arquivos:
                    texto_total += ler_pdf(arq) + "\n"
                
                # 2. IA Gera o DNA
                dna_gerado = analisar_dna_cliente(api_key, texto_total, nuances)
                
                # 3. Salvar
                st.session_state['agencias'][nome_empresa] = dna_gerado
                
                st.success(f"✅ Agência '{nome_empresa}' calibrada com sucesso!")
                st.markdown("### 📑 Perfil Técnico Gerado:")
                st.info(dna_gerado)

    # Mostrar Agências Ativas
    if st.session_state['agencias']:
        st.divider()
        st.subheader("🌌 Frotas Disponíveis:")
        st.write(list(st.session_state['agencias'].keys()))

# ==================================================
# SISTEMA 2: LANÇAMENTO (ANÁLISE DE EDITAL)
# ==================================================
elif opcao == "2. Lançamento (Analisar Missão)":
    st.header("🪐 Simulação de Lançamento (Análise de Edital)")
    
    if not st.session_state['agencias']:
        st.warning("⚠️ Nenhuma frota detectada. Vá ao Hangar primeiro.")
        st.stop()
    
    # Selecionar Nave
    agencia_escolhida = st.selectbox("🚀 Selecionar Nave para a Missão:", list(st.session_state['agencias'].keys()))
    
    # Expander discreto para ver o DNA se precisar
    with st.expander(f"🔍 Ver DNA Técnico: {agencia_escolhida}"):
        st.text(st.session_state['agencias'][agencia_escolhida])
        
    st.divider()
    
    # Upload da Missão
    edital = st.file_uploader("📜 Carregar Edital da Missão (PDF)", type="pdf")
    
    if st.button("🔴 INICIAR ANÁLISE FORENSE"):
        if not edital:
            st.error("⚠️ Edital não detectado.")
        else:
            with st.spinner(f"🛰️ Cruzando dados da {agencia_escolhida} com exigências do Edital..."):
                texto_edital = ler_pdf(edital)
                dna_atual = st.session_state['agencias'][agencia_escolhida]
                
                # IA Analisa
                resultado = analisar_edital_com_dna(api_key, texto_edital, dna_atual)
                
                st.markdown("---")
                # Exibe o resultado
                st.markdown(resultado)
