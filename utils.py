import streamlit as st
import pandas as pd
from utils import ler_pdf, analisar_dna_cliente, analisar_edital_com_dna

# --- CONFIGURAÇÃO DO COCKPIT ---
st.set_page_config(page_title="Apollo Mission Control", page_icon="🚀", layout="wide")

# Cabeçalho Espacial
st.title("🚀 Projeto Apollo: Controle de Missão")
st.markdown("**Status:** Sistema Operacional | **Versão:** 2.0 (Deep Space)")

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
    st.header("🛸 Hangar: Configuração da Frota")
    st.info("Cadastre as especificações técnicas da sua Agência Espacial (Empresa).")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_empresa = st.text_input("Nome da Agência (Empresa)")
        nuances = st.text_area("Diretrizes da Base (O que vocês fazem de melhor?)", 
            placeholder="Ex: Especialistas em propulsão (obras civis), mas terceirizamos o suporte de vida (elétrica).",
            height=150)
            
    with col2:
        st.write("📂 **Planos e Certificações (PDFs)**")
        st.write("(Contratos Sociais, Atestados Técnicos)")
        arquivos = st.file_uploader("Carregar Arquivos de Sistema", type="pdf", accept_multiple_files=True)

    if st.button("🛠️ Construir Manual da Nave"):
        if not api_key:
            st.error("⚠️ Chave de Acesso não inserida nos propulsores!")
        elif not nome_empresa or not arquivos:
            st.warning("⚠️ Dados insuficientes para decolagem.")
        else:
            with st.spinner("🔄 Processando telemetria e compilando dados..."):
                # 1. Processar Documentos
                texto_total = ""
                for arq in arquivos:
                    texto_total += ler_pdf(arq) + "\n"
                
                # 2. IA Gera o DNA
                dna_gerado = analisar_dna_cliente(api_key, texto_total, nuances)
                
                # 3. Salvar
                st.session_state['agencias'][nome_empresa] = dna_gerado
                
                st.success(f"✅ Agência '{nome_empresa}' registrada no sistema Apollo!")
                st.markdown("### 📄 Manual de Voo Gerado:")
                st.write(dna_gerado)

    # Mostrar Agências Ativas
    if st.session_state['agencias']:
        st.divider()
        st.subheader("🌌 Frotas Disponíveis:")
        st.write(list(st.session_state['agencias'].keys()))

# ==================================================
# SISTEMA 2: LANÇAMENTO (ANÁLISE DE EDITAL)
# ==================================================
elif opcao == "2. Lançamento (Analisar Missão)":
    st.header("🪐 Simulação de Missão (Análise de Edital)")
    
    if not st.session_state['agencias']:
        st.warning("⚠️ Nenhuma frota detectada. Vá ao Hangar primeiro.")
        st.stop()
    
    # Selecionar Nave
    agencia_escolhida = st.selectbox("🚀 Selecionar Nave para a Missão:", list(st.session_state['agencias'].keys()))
    
    with st.expander(f"🔍 Ver Especificações da {agencia_escolhida}"):
        st.write(st.session_state['agencias'][agencia_escolhida])
        
    st.divider()
    
    # Upload da Missão
    edital = st.file_uploader("📜 Carregar Parâmetros da Missão (Edital PDF)", type="pdf")
    
    if st.button("🔴 INICIAR CONTAGEM REGRESSIVA (Analisar)"):
        if not edital:
            st.error("⚠️ Parâmetros da missão não encontrados (Falta PDF).")
        else:
            with st.spinner(f"🛰️ Computador central calculando trajetória para {agencia_escolhida}..."):
                texto_edital = ler_pdf(edital)
                dna_atual = st.session_state['agencias'][agencia_escolhida]
                
                # IA Analisa
                resultado = analisar_edital_com_dna(api_key, texto_edital, dna_atual)
                
                st.markdown("---")
                st.subheader("📡 Relatório de Viabilidade da Missão")
                st.markdown(resultado)
