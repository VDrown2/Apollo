import google.generativeai as genai
import PyPDF2

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

def diagnostico_modelos():
    """Lista quais motores estão disponíveis no hangar."""
    try:
        modelos = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modelos.append(m.name)
        return modelos
    except Exception as e:
        return [f"Erro ao listar modelos: {e}"]

def analisar_dna_cliente(api_key, documentos_texto, nuances):
    """Módulo A: Registro da Agência Espacial."""
    if not api_key: return "ERRO: Chave de Acesso não detectada."
    
    genai.configure(api_key=api_key)
    
    # MANOBRA DE EMERGÊNCIA: Usando modelo clássico
    modelo_escolhido = 'gemini-pro'
    
    try:
        model = genai.GenerativeModel(modelo_escolhido) 
        prompt = f"""
        ATUE COMO: Engenheiro Chefe da NASA.
        MISSÃO: Criar DNA Técnico da empresa.
        NUANCES: "{nuances}"
        DOCUMENTOS: {documentos_texto[:300000]}
        SAÍDA: Liste Áreas de Domínio, Maiores Atestados e Restrições.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Se der erro, ele vai listar o que está disponível
        lista = diagnostico_modelos()
        return f"⚠️ FALHA NO MOTOR {modelo_escolhido}. \n\nErro técnico: {e}\n\n✅ MOTORES DISPONÍVEIS NA SUA CONTA: {lista}"

def analisar_edital_com_dna(api_key, texto_edital, dna_cliente):
    """Módulo B: Simulação de Missão."""
    if not api_key: return "ERRO: Chave de Acesso não detectada."

    genai.configure(api_key=api_key)
    
    # MANOBRA DE EMERGÊNCIA: Usando modelo clássico
    modelo_escolhido = 'gemini-pro'
    
    try:
        model = genai.GenerativeModel(modelo_escolhido)
        prompt = f"""
        ATUE COMO: Diretor de Voo da Missão Apollo.
        CAPACIDADE DA NAVE: {dna_cliente}
        EDITAL DA MISSÃO: {texto_edital[:300000]}
        
        RELATÓRIO DE VOO:
        1. Status (GO / NO-GO)
        2. Riscos Críticos (🔴/🟡/🟢)
        3. Jurídico e Financeiro
        4. Plano de Voo
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        lista = diagnostico_modelos()
        return f"⚠️ FALHA NO MOTOR {modelo_escolhido}. \n\nErro técnico: {e}\n\n✅ MOTORES DISPONÍVEIS NA SUA CONTA: {lista}"
