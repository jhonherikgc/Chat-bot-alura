# 🤖 InteliBot – Chatbot com Gemini AI

**InteliBot** é um assistente virtual inteligente construído com **Flask** e integrado aos modelos **Gemini (Google Generative AI)**. Ele permite ao usuário conversar com a IA, receber respostas com código formatado, e ainda simula uma animação de digitação para uma experiência mais fluida e realista.

---

## 🚀 Tecnologias Utilizadas

- **[Flask](https://flask.palletsprojects.com/)** — Framework web em Python
- **[Google Generative AI (Gemini)](https://ai.google.dev/)** — API de modelos de linguagem
- **[Flask-Session](https://pythonhosted.org/Flask-Session/)** — Gerenciamento de sessões para memória do chat
- **[TailwindCSS](https://tailwindcss.com/)** — Estilização moderna e responsiva
- **HTML + CSS + JavaScript** — Frontend dinâmico
- **Efeitos JS personalizados** — Animação de digitação para respostas
- **Renderização de código formatado** — Usando `<pre><code>` para blocos de código

---

## 📸 Funcionalidades

- ✅ Interface intuitiva e responsiva
- ✅ Escolha entre modelos Gemini 1.5 e 2.0
- ✅ Memória de conversas (durante a sessão)
- ✅ Código retornado formatado corretamente
- ✅ Efeitos de digitação em tempo real
- ✅ Totalmente customizável com CSS/JS

---

## 🛠️ Como Rodar Localmente

### Pré-requisitos:

- Python 3.10+
- Conta na [Google Generative AI](https://makersuite.google.com/app) com chave de API
- Node opcionalmente (para custom builds de CSS, se desejar)

### Passos:

```bash
# 1. Clone o repositório
git clone https://github.com/seuusuario/intelibot.git
cd intelibot

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Adicione a chave da API em um arquivo .env
echo "GOOGLE_API_KEY=sua-chave-aqui" > .env

# 5. Execute o app
python app.py
```
### 🙏 Agradecimentos
Este projeto foi desenvolvido com base no aprendizado da Imersão Inteligência Artificial 2025 da Alura.
A imersão me guiou passo a passo na criação do projeto, na integração com IA generativa e construção do frontend moderno.

Obrigado à equipe da Alura pela didática incrível e por compartilhar tanto conhecimento! 💙

---