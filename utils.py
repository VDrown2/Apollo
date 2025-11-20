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
    """Módulo A: Criação do Perfil Técnico."""
    if not api_key: return "ERRO: Chave de Acesso não detectada."
    
    genai.configure(api_key=api_key)
    modelo_escolhido = 'gemini-2.5-flash'
    
    try:
        model = genai.GenerativeModel(modelo_escolhido) 
        prompt = f"""
        ATUE COMO: Auditor Técnico de Engenharia.
        OBJETIVO: Criar Perfil Técnico da empresa.
        
        DIRETRIZES: "{nuances}"
        ACERVO: {documentos_texto[:300000]}
        
        SAÍDA:
        1. Matriz de Competência (O que fazem).
        2. Destaques do Acervo (Maiores obras).
        3. Mapa de Restrições (O que não fazem).
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        lista = diagnostico_modelos()
        return f"⚠️ FALHA NO MOTOR {modelo_escolhido}. \n\nErro: {e}\n\n✅ DISPONÍVEIS: {lista}"

def analisar_edital_com_dna(api_key, texto_edital, dna_cliente):
    """Módulo B: Análise em 3 Estágios com Separadores Robustos."""
    if not api_key: return "ERRO: Chave de Acesso não detectada."

    genai.configure(api_key=api_key)
    modelo_escolhido = 'gemini-2.5-flash'
    
    try:
        model = genai.GenerativeModel(modelo_escolhido)
        prompt = f"""
        ATUE COMO: Consultor Sênior de Licitações.
        CONTEXTO (DNA): {dna_cliente}
        EDITAL: {texto_edital[:300000]}
        
        SUA MISSÃO: Gerar 3 relatórios em sequência. É CRUCIAL usar as tags de separação exatas abaixo.
        
        ---
        PARTE 1: IMPEDITIVOS CRÍTICOS (O "Matador" de Proposta)
        Objetivo: Identificar IMEDIATAMENTE se devemos abortar.
        Conteúdo:
        # 🛑 ANÁLISE DE RISCO FATAL
        * **Veredito Rápido:** [GO / NO-GO / RISCO]
        * **Impeditivos Técnicos:** (Liste apenas o que a empresa NÃO tem e o edital exige. Se não houver, diga "Nenhum").
        * **Impeditivos Jurídicos:** (Índices inalcançáveis, falência, etc).
        
        ESCREVA A TAG DE SEPARAÇÃO 1 ABAIXO (Sem negrito):
        |||SEP_CONSULTOR|||
        
        PARTE 2: DOSSIÊ TÉCNICO (Para o Consultor/Engenheiro)
        Objetivo: Detalhar a montagem da proposta.
        Conteúdo:
        # 👷‍♂️ ANÁLISE TÉCNICA DETALHADA
        ## 1. Checklist de Habilitação
        (Tabela comparativa item a item: Edital vs DNA).
        ## 2. Documentos Específicos
        (O que precisa separar agora? Atestados, Certidões, Balanço).
        ## 3. Pontos de Atenção
        (Multas, Prazos, Garantia).
        
        ESCREVA A TAG DE SEPARAÇÃO 2 ABAIXO (Sem negrito):
        |||SEP_CLIENTE|||
        
        PARTE 3: RESUMO EXECUTIVO (Para o Dono/Cliente)
        Objetivo: Texto simples para WhatsApp/Email.
        Conteúdo:
        # 👔 RESUMO PARA DIRETORIA
        * **Oportunidade:** (Resumo do objeto e valor).
        * **Nossa Situação:** (Temos atestado? Sim/Não).
        * **Recomendação:** (Participar ou não, e porquê, em 1 frase simples).
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        lista = diagnostico_modelos()
        return f"⚠️ FALHA NO MOTOR {modelo_escolhido}. \n\nErro: {e}\n\n✅ DISPONÍVEIS: {lista}"
