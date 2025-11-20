import google.generativeai as genai
import PyPDF2

def ler_pdf(uploaded_file):
    """Extrai texto dos arquivos PDF."""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Erro na leitura do arquivo: {e}"

def diagnostico_modelos():
    """Lista quais motores estão disponíveis."""
    try:
        modelos = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modelos.append(m.name)
        return modelos
    except Exception as e:
        return [f"Erro ao listar modelos: {e}"]

def analisar_dna_cliente(api_key, documentos_texto, nuances):
    """Módulo A: Criação do Perfil Técnico (Sério)."""
    if not api_key: return "ERRO: Chave de Acesso não detectada."
    
    genai.configure(api_key=api_key)
    
    # Mantendo o motor potente que funcionou para você
    modelo_escolhido = 'gemini-2.5-flash'
    
    try:
        model = genai.GenerativeModel(modelo_escolhido) 
        prompt = f"""
        ATUE COMO: Auditor Técnico de Engenharia e Licitações.
        OBJETIVO: Mapear a Capacidade Técnica Operacional da empresa com base em documentos comprobatórios.
        
        DIRETRIZES ESTRATÉGICAS (O que o diretoria informou):
        "{nuances}"
        
        ACERVO TÉCNICO (Atestados e Contratos):
        {documentos_texto[:300000]}
        
        SAÍDA OBRIGATÓRIA (Use linguagem técnica e formal):
        
        ## 1. Matriz de Competência
        (Liste as áreas de engenharia/serviço onde a empresa possui atestação robusta).
        
        ## 2. Destaques do Acervo
        (Liste os 3 maiores contratos/obras realizados, citando quantitativos se houver).
        
        ## 3. Mapa de Restrições (Gap Analysis)
        (O que a empresa NÃO comprova tecnicamente ou precisa subcontratar? Baseie-se na ausência de atestados para certas atividades citadas nas nuances).
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        lista = diagnostico_modelos()
        return f"⚠️ FALHA NO MOTOR {modelo_escolhido}. \n\nErro técnico: {e}\n\n✅ MOTORES DISPONÍVEIS: {lista}"

def analisar_edital_com_dna(api_key, texto_edital, dna_cliente):
    """Módulo B: Análise de Licitação (Dividida em Visão Cliente e Visão Consultor)."""
    if not api_key: return "ERRO: Chave de Acesso não detectada."

    genai.configure(api_key=api_key)
    modelo_escolhido = 'gemini-2.5-flash'
    
    try:
        model = genai.GenerativeModel(modelo_escolhido)
        prompt = f"""
        ATUE COMO: Consultor Sênior de Licitações Públicas.
        CONTEXTO DA EMPRESA (DNA): {dna_cliente}
        EDITAL EM ANÁLISE: {texto_edital[:300000]}
        
        SUA MISSÃO: Analisar a viabilidade e os riscos desta licitação.
        
        GERE O RELATÓRIO EXATAMENTE COM AS SEÇÕES ABAIXO:
        
        ---
        
        # 🛑 VEREDITO FINAL: [GO / NO-GO / GO-COM-RISCO]
        (Justificativa em 1 parágrafo direto).
        
        ---
        
        # 💼 SEÇÃO 1: RESUMO EXECUTIVO (PARA O CLIENTE LER)
        *Escreva simples. O dono da empresa vai ler isso no celular.*
        * **O que é:** (Resumo do objeto).
        * **Quanto:** (Valor estimado, se houver).
        * **Quando:** (Data da disputa).
        * **Principais Riscos:** (Resumo dos 2 maiores problemas, sem tecniquês).
        
        ---
        
        # 🕵️‍♂️ SEÇÃO 2: ANÁLISE TÉCNICA PROFUNDA (PARA O CONSULTOR)
        *Aqui você deve ser técnico, jurídico e detalhista.*
        
        ## A. Habilitação Técnica (Onde podemos cair)
        * Compare item a item do DNA com o Edital.
        * Use emojis: 🔴 (Falta Atestado), 🟡 (Atestado Parcial/Dúvida), 🟢 (Atendemos).
        * Cite a página ou item do edital onde está a exigência.
        
        ## B. Armadilhas Jurídicas e Financeiras
        * Índices contábeis exigidos (LG, SG, IL).
        * Exigências de garantia incomuns.
        * Multas abusivas.
        
        ## C. Plano de Ação do Consultor
        * Liste documentos específicos que precisam ser montados.
        * Sugestão de Pedido de Esclarecimento ou Impugnação (se houver cláusulas restritivas).
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        lista = diagnostico_modelos()
        return f"⚠️ FALHA NO MOTOR {modelo_escolhido}. \n\nErro técnico: {e}\n\n✅ MOTORES DISPONÍVEIS: {lista}"
