import google.generativeai as genai
import PyPDF2
import io

def ler_pdf(uploaded_file):
    """Lê o PDF e transforma em texto puro."""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Erro ao ler PDF: {e}"

def analisar_dna_cliente(api_key, documentos_texto, nuances):
    """
    Módulo A: Ingestão do DNA.
    Cria o REC (Resumo Estruturado de Capacidade).
    """
    if not api_key:
        return "ERRO: API Key não configurada."
        
    genai.configure(api_key=api_key)
    # Usamos o Gemini 1.5 Flash que é rápido e inteligente o suficiente para resumos
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    prompt = f"""
    ATUE COMO: Consultor Sênior de Licitações e Engenharia.
    
    TAREFA: Criar um "DNA Técnico" (Resumo Estruturado de Capacidade - REC) desta empresa.
    
    1. O QUE O DONO DA EMPRESA DISSE (NUANCES):
    "{nuances}"
    
    2. O QUE ESTÁ NOS ATESTADOS E CONTRATOS (DOCUMENTOS):
    {documentos_texto[:400000]} 
    
    SAÍDA ESPERADA (Responda apenas com o resumo):
    Analise os documentos e crie um perfil técnico robusto.
    - Liste as Áreas de Domínio (o que eles comprovadamente fazem).
    - Liste os Maiores Atestados (Ex: "Obra de 500m²", "Fornecimento de 1000 itens").
    - Liste RESTRIÇÕES: O que eles NÃO fazem ou precisam terceirizar (baseado nas nuances e falta de atestados).
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro na IA: {e}"

def analisar_edital_com_dna(api_key, texto_edital, dna_cliente):
    """
    Módulo B: Cross-Match (Edital vs DNA).
    """
    if not api_key:
        return "ERRO: API Key não configurada."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    ATUE COMO: Consultor Jurídico e Técnico de Licitações (Forensic Bid Analyst).
    
    CONTEXTO DO SEU CLIENTE (O DNA): 
    {dna_cliente}
    
    DOCUMENTO PARA ANÁLISE (EDITAL):
    {texto_edital[:800000]}
    
    SUA MISSÃO: 
    Faça o "Cross-Match" (Confronto) entre o que o edital pede e o que o cliente tem.
    
    GERE UM RELATÓRIO NO SEGUINTE FORMATO:
    
    ## 1. Veredito Rápido
    (Diga GO, NO-GO ou GO-COM-RISCO e explique em 1 frase).
    
    ## 2. Análise de Habilitação Técnica (Onde mora o perigo)
    - Compare cada exigência técnica do edital com o DNA do cliente.
    - Se o edital pede algo que o DNA não tem, marque com 🔴 [CRÍTICO].
    - Se o edital pede algo que o DNA tem parcialmente, marque com 🟡 [ATENÇÃO].
    - Se o DNA atende, marque com 🟢 [OK].
    
    ## 3. Pontos de Atenção Jurídica/Financeira
    (Resuma garantias, prazos, multas pesadas).
    
    ## 4. Sugestão de Ação
    (O que o consultor deve fazer agora? Ex: "Buscar parceiro para item X").
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro na IA: {e}"
