import google.generativeai as genai
import PyPDF2
import io

def ler_pdf(uploaded_file):
    """Extrai a telemetria (texto) dos arquivos PDF."""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Erro na leitura dos sensores PDF: {e}"

def analisar_dna_cliente(api_key, documentos_texto, nuances):
    """
    Módulo A: Registro da Agência Espacial.
    """
    if not api_key: return "ERRO: Chave de Acesso não detectada."
    
    genai.configure(api_key=api_key)
    # Usando a versão estável 001
    model = genai.GenerativeModel('gemini-1.5-flash-001') 
    
    prompt = f"""
    ATUE COMO: Engenheiro Chefe da NASA e Especialista em Licitações.
    
    MISSÃO: Criar o "Manual de Voo" (DNA Técnico) desta Agência (Empresa).
    
    DIRETRIZES DA BASE (O que o comandante disse):
    "{nuances}"
    
    REGISTROS DE VOO ANTERIORES (Atestados e Contratos):
    {documentos_texto[:400000]} 
    
    SAÍDA ESPERADA:
    Analise a capacidade desta agência espacial.
    - Capacidade de Propulsão (O que a empresa domina).
    - Histórico de Lançamentos (Maiores obras/contratos realizados).
    - Limitações de Órbita (O que ela NÃO faz ou precisa de suporte externo).
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Falha na comunicação com a IA: {e}"

def analisar_edital_com_dna(api_key, texto_edital, dna_cliente):
    """
    Módulo B: Simulação de Missão (Edital vs DNA).
    """
    if not api_key: return "ERRO: Chave de Acesso não detectada."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-001')
    
    prompt = f"""
    ATUE COMO: Diretor de Voo (Flight Director) da Missão Apollo.
    
    CAPACIDADE DA NAVE (DNA DA EMPRESA): 
    {dna_cliente}
    
    PARÂMETROS DA MISSÃO (EDITAL):
    {texto_edital[:800000]}
    
    SUA MISSÃO: 
    Simule o lançamento desta missão (participação na licitação). Cruze os requisitos da missão com a capacidade da nave.
    
    RELATÓRIO DE VOO:
    
    ## 1. Status de Lançamento (GO / NO-GO)
    (Dê o veredito final e explique em linguagem de comando).
    
    ## 2. Telemetria Técnica (Riscos Críticos)
    - Compare o edital com a empresa.
    - Se faltar um requisito obrigatório: 🔴 [ABORTAR] (Explique o motivo).
    - Se for arriscado mas possível: 🟡 [ALERTA DE COLISÃO].
    - Se estiver tudo certo: 🟢 [PROPULSÃO ESTÁVEL].
    
    ## 3. Sistemas Jurídicos e Financeiros
    (Analise multas, garantias e prazos como se fossem combustível e escudos).
    
    ## 4. Plano de Voo Sugerido
    (Recomendação tática para o comandante da empresa).
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Perda de sinal com a IA: {e}"
