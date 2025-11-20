import streamlit as st
import pandas as pd
from utils import ler_pdf, analisar_dna_cliente, analisar_edital_com_dna

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="LicitaAI Pro", page_icon="⚖️", layout="wide")

# Título Principal
st.title("⚖️ LicitaAI: Sistema de Inteligência para Licitações")
st.markdown("Referência: Cenário 2 - O Caminho Profissional de Baixo Custo")

# --- BARRA LATERAL ---
st.sidebar.header("Navegação")
opcao = st.sidebar.radio("Escolha a etapa:", ["1. DNA do Cliente (Cadastro)", "2. Análise de Edital (Mão na Massa)"])

# Pegando a Chave Secreta (Vamos configurar isso no passo final)
# Se não achar a chave secreta, pede na tela (bom para testes)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Cole sua API Key do Google aqui:", type="password")

# --- MEMÓRIA DO SISTEMA ---
# Como não estamos usando Banco de Dados real ainda, usamos a memória do navegador
if 'clientes' not in st.session_state:
    st.session_state['clientes'] = {} # Dicionário vazio para guardar clientes

# ==================================================
# TELA 1: CADASTRO DE DNA (O PERFIL TÉCNICO)
# ==================================================
if opcao == "1. DNA do Cliente (Cadastro)":
    st.header("🧬 Módulo A: DNA do Cliente")
    st.info("Aqui você ensina a IA sobre a empresa. Faça isso apenas uma vez por cliente.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_empresa = st.text_input("Nome da Empresa/Cliente")
        nuances = st.text_area("Nuances e 'Jeito de Trabalhar'", 
            placeholder="Ex: Somos fortes em obras civis, mas não temos engenheiro mecânico. Terceirizamos ar-condicionado.",
            height=150)
            
    with col2:
        st.write("📂 **Upload de Documentos Prova**")
        st.write("(Contrato Social, Atestados de Capacidade, Balanços)")
        arquivos = st.file_uploader("Selecione os PDFs", type="pdf", accept_multiple_files=True)

    if st.button("Gerar DNA Técnico"):
        if not api_key:
            st.error("Coloque a API Key na barra lateral!")
        elif not nome_empresa or not arquivos:
            st.warning("Preencha o nome e suba arquivos.")
        else:
            with st.spinner("Lendo documentos e criando perfil... (Isso pode levar uns segundos)"):
                # 1. Juntar todo texto dos PDFs
                texto_total = ""
                for arq in arquivos:
                    texto_total += ler_pdf(arq) + "\n"
                
                # 2. Chamar a IA
                dna_gerado = analisar_dna_cliente(api_key, texto_total, nuances)
                
                # 3. Salvar na memória
                st.session_state['clientes'][nome_empresa] = dna_gerado
                
                st.success(f"DNA da '{nome_empresa}' criado e salvo na memória!")
                st.markdown("### 📝 Resumo Gerado (DNA):")
                st.write(dna_gerado)

    # Mostrar quem já está na memória
    if st.session_state['clientes']:
        st.divider()
        st.subheader("Clientes na Memória Atual:")
        st.write(list(st.session_state['clientes'].keys()))

# ==================================================
# TELA 2: ANÁLISE DE EDITAL (O DIA A DIA)
# ==================================================
elif opcao == "2. Análise de Edital (Mão na Massa)":
    st.header("🔎 Módulo B: Análise Forense de Edital")
    
    # Verifica se tem cliente cadastrado
    if not st.session_state['clientes']:
        st.warning("⚠️ Você ainda não cadastrou nenhum cliente no Módulo 1.")
        st.stop()
    
    # Selecionar Cliente
    cliente_escolhido = st.selectbox("Para qual cliente é esta licitação?", list(st.session_state['clientes'].keys()))
    
    # Mostrar DNA escondido (Expander)
    with st.expander(f"Ver DNA carregado de: {cliente_escolhido}"):
        st.write(st.session_state['clientes'][cliente_escolhido])
        
    st.divider()
    
    # Upload do Edital
    edital = st.file_uploader("📄 Suba o Edital ou Termo de Referência (PDF)", type="pdf")
    
    if st.button("Analisar Riscos e Oportunidades"):
        if not edital:
            st.error("Preciso do PDF do edital!")
        else:
            with st.spinner(f"A IA está lendo o edital e cruzando com o perfil da {cliente_escolhido}..."):
                texto_edital = ler_pdf(edital)
                dna_atual = st.session_state['clientes'][cliente_escolhido]
                
                # Chama a IA para cruzar os dados
                resultado = analisar_edital_com_dna(api_key, texto_edital, dna_atual)
                
                st.markdown("---")
                st.subheader("📊 Relatório de Inteligência")
                st.markdown(resultado)
