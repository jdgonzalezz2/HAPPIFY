import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Flask y CORS
app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# Configurar el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Historial de conversación
messages = [
    {"role": "system", "content": "Eres un consejero emocional experto. Tu trabajo es en primera instancia dar consejos que puedan ayudar a las peticiones del usuario. A continuación harás unas preguntas o reflexiones que hagan al usuario reflexionar sobre sí mismo. Después, debes redirigir al usuario al profesional que más le convenga. Si es posible haz preguntas para que la conversación pueda fluir. Debes tener mucho cuidado al tratar temas muy sensibles, prioriza la vida y el bienestar del usuario ante todo."}
]

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        chat_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": chat_reply})
        return jsonify({"reply": chat_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Programa principal
if __name__ == "__main__":
    app.run(debug=True, port=5000)
