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
    # Usando o modelo mais estável disponível
    modelo_escolhido = 'gemini-2.5-flash'
    
    try:
        model = genai.GenerativeModel(modelo_escolhido) 
        prompt = f"""
        ATUE COMO: Auditor Técnico de Engenharia.
        OBJETIVO: Criar Perfil Técnico da empresa (EUCAPISO ou similar).
        
        DIRETRIZES ESTRATÉGICAS: "{nuances}"
        ACERVO TÉCNICO: {documentos_texto[:300000]}
        
        SAÍDA:
        1. Pontos Fortes (Atestados, CNAEs, Capacidade).
        2. Pontos Fracos/Impeditivos (O que não faz, restrições).
        3. Dados Financeiros (Se houver no texto).
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        lista = diagnostico_modelos()
        return f"⚠️ FALHA NO MOTOR {modelo_escolhido}. \n\nErro: {e}\n\n✅ DISPONÍVEIS: {lista}"

def analisar_edital_com_dna(api_key, texto_edital, dna_cliente):
    """Módulo B: Análise Profunda com Super Prompt."""
    if not api_key: return "ERRO: Chave de Acesso não detectada."

    genai.configure(api_key=api_key)
    modelo_escolhido = 'gemini-2.5-flash'
    
    try:
        model = genai.GenerativeModel(modelo_escolhido)
        
        # O SEU SUPER PROMPT COMEÇA AQUI
        prompt = f"""
        "A partir de agora, você atuará como Analista de Risco e Consultor Estratégico de Licitações. Siga todas as regras rigorosamente."

        1. CONTEXTO E MISSÃO
        Sua especialidade é dissecação forense de editais e análise de gaps.
        Você deve comparar o EDITAL fornecido com o PERFIL DO CLIENTE abaixo.

        ---
        3. PERFIL DO CLIENTE (DNA)
        {dna_cliente}
        ---

        5. DOCUMENTO A ANALISAR (EDITAL/TR)
        {texto_edital[:400000]}
        ---

        7. FORMATO DE SAÍDA (OBRIGATÓRIO - 3 BLOCOS SEPARADOS)
        
        Você deve gerar a resposta dividida EXATAMENTE pelas tags de separação indicadas.

        🎯 BLOCO 1: ALERTA DE RISCO (Análise de Gaps)
        Conteúdo:
        * PONTOS DE IMPUGNAÇÃO (Ação Imediata - Ilegalidades, Marcas).
        * IMPEDITIVOS (Bloqueadores Vermelhos - Ex: CREA, Balanço ruim).
        * PROBLEMAS (Riscos Altos Amarelos).
        * OPORTUNIDADES (Pontos Fortes Verdes).
        
        (Regra: Cite sempre o Item/Anexo da fonte).

        AGORA, ESCREVA EXATAMENTE A TAG DE SEPARAÇÃO ABAIXO (Sem negrito):
        |||SEP_CONSULTOR|||

        📊 BLOCO 2: ANÁLISE TÉCNICA INTERNA (Para o Consultor)
        Conteúdo:
        ANÁLISE DO PROCESSO: [Nº e ano]
        1. Análise Direta (Checklist Rápido: Órgão, Portal, Data, Critério, Valor, Visita, etc).
        2. Análise Reversa (Exigências e Prazos: Objeto detalhado, Habilitação Jurídica/Técnica/Fiscal/Econômica).
        3. Exigências Pós-Homologação e Minuta de Contrato.
        
        AGORA, ESCREVA EXATAMENTE A TAG DE SEPARAÇÃO ABAIXO (Sem negrito):
        |||SEP_CLIENTE|||

        📄 BLOCO 3: RESUMO EXECUTIVO (Para o Cliente Final)
        Conteúdo:
        "Olá, equipe [Nome do Cliente]."
        * Oportunidade: [Órgão] - [Objeto Resumido]
        * Licitação: [Número]
        * Data da Disputa: [Data/Hora]
        * Exigências-Chave (Apenas o que foge do padrão e requer atenção do dono).
        * Veredito Simples.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        lista = diagnostico_modelos()
        return f"⚠️ FALHA NO MOTOR {modelo_escolhido}. \n\nErro: {e}\n\n✅ DISPONÍVEIS: {lista}"
