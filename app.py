from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import os
from dotenv import load_dotenv
import google.generativeai as genai
import warnings

warnings.filterwarnings("ignore")

# Carrega variáveis de ambiente
load_dotenv()

# Configura chave da API
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)

# Inicializa o Flask
app = Flask(__name__)
app.secret_key = 'sua-chave-secreta'  # Use uma chave forte em produção
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Gera a resposta do modelo com memória
@app.route('/gerar_resposta', methods=['POST'])
def gerar_resposta():
    pergunta = request.form['pergunta']
    modelo_selecionado = request.form['modelo']

    # Recupera ou inicia o histórico
    historico = session.get('historico', [])

    # Adiciona a pergunta do usuário
    historico.append({'role': 'user', 'parts': [pergunta]})

    try:
        model = genai.GenerativeModel(modelo_selecionado)

        # Gera resposta com o histórico completo
        resposta = model.generate_content(contents=historico)
        texto_resposta = resposta.text if resposta and resposta.text else "Sem resposta do modelo."

        # Adiciona a resposta do modelo
        historico.append({'role': 'model', 'parts': [texto_resposta]})
        session['historico'] = historico  # Salva o histórico atualizado

        return jsonify({'resposta': texto_resposta, 'model': modelo_selecionado})

    except Exception as e:
        return jsonify({'erro': f"Ocorreu um erro ao gerar a resposta: {e}"})

# Opcional: rota para limpar o histórico da sessão
@app.route('/limpar_historico')
def limpar_historico():
    session.pop('historico', None)
    return 'Histórico limpo!'

if __name__ == '__main__':
    app.run(debug=True)
