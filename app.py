from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Configura o sistema de logging para exibir mensagens de DEBUG e INFO
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega variáveis de ambiente
load_dotenv()

# Configura chave da API
google_api_key = os.getenv('GOOGLE_API_KEY')
if not google_api_key:
    logging.error("GOOGLE_API_KEY não encontrada nas variáveis de ambiente. Por favor, verifique seu arquivo .env")
    # Você pode optar por levantar uma exceção aqui ou lidar com isso de outra forma
else:
    genai.configure(api_key=google_api_key)
    logging.info("Google Generative AI configurado com sucesso.")

# Inicializa o Flask
app = Flask(__name__)
app.secret_key = 'sua-chave-secreta'  # Use uma chave forte em produção
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Removendo o filtro de warnings temporariamente para depuração
# warnings.filterwarnings("ignore") # Descomente se quiser ignorar warnings após a depuração

# Rota principal
@app.route('/')
def index():
    logging.info("Página inicial acessada.")
    return render_template('index.html')
                                                
# Gera a resposta do modelo com memória
@app.route('/gerar_resposta', methods=['POST'])         
def gerar_resposta():
    pergunta = request.form['pergunta']
    modelo_selecionado = request.form['modelo'] 
    logging.debug(f"Recebida pergunta: '{pergunta}' para o modelo: '{modelo_selecionado}'")

    # Recupera ou inicia o histórico
    historico = session.get('historico', [])
    logging.debug(f"Histórico atual da sessão: {historico}")

    # Adiciona a pergunta do usuário
    historico.append({'role': 'user', 'parts': [pergunta]})

    try:
        model = genai.GenerativeModel('gemini-1.0-pro')
        model = genai.GenerativeModel(modelo_selecionado)
        logging.debug(f"Modelo Generative AI instanciado: {modelo_selecionado}")

        # Gera resposta com o histórico completo
        logging.debug("Chamando model.generate_content...")
        resposta = model.generate_content(contents=historico)
        logging.debug(f"Resposta bruta da API: {resposta}")
        
        texto_resposta = "Não foi possível extrair uma resposta do modelo. A resposta pode estar vazia ou bloqueada." # Mensagem padrão
        try:
            # Acessa o texto da primeira parte da primeira candidata
            if resposta and resposta.candidates and len(resposta.candidates) > 0 and \
               resposta.candidates[0].content and resposta.candidates[0].content.parts and \
               len(resposta.candidates[0].content.parts) > 0:
                texto_resposta = resposta.candidates[0].content.parts[0].text
                logging.info(f"Texto da resposta extraído com sucesso: {texto_resposta[:100]}...") # Log dos primeiros 100 caracteres
            else:
                logging.warning(f"Resposta da API não contém texto extraível ou está vazia. Resposta completa: {resposta}")
        except (IndexError, AttributeError) as e:
            logging.error(f"Erro ao tentar extrair texto da resposta: {e}", exc_info=True)

        # Adiciona a resposta do modelo
        historico.append({'role': 'model', 'parts': [texto_resposta]})
        session['historico'] = historico  # Salva o histórico atualizado

        return jsonify({'resposta': texto_resposta, 'model': modelo_selecionado})

    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado ao gerar a resposta: {e}", exc_info=True)
        return jsonify({'erro': f"Ocorreu um erro no servidor ao gerar a resposta: {e}"})

# Opcional: rota para limpar o histórico da sessão
@app.route('/limpar_historico')
def limpar_historico():
    session.pop('historico', None)
    return 'Histórico limpo!'

if __name__ == '__main__':
    app.run(debug=True)
