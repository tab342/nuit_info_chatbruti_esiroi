from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
from test import ChatbotGemma

app = Flask(__name__)
CORS(app)

# Initialiser le chatbot
chatbot = ChatbotGemma(model_name="gemma3:1b")

# Template HTML
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💬 Chat'bruti</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 900px;
            background: #0d1117;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 90vh;
        }

        .header {
            background: linear-gradient(135deg, #161b22 0%, #21262d 100%);
            padding: 30px;
            text-align: center;
            border-bottom: 2px solid #30363d;
        }

        .header h1 {
            color: #58a6ff;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(88, 166, 255, 0.3);
        }

        .header p {
            color: #8b949e;
            font-size: 1.1em;
        }

        .chat-container {
            flex: 1;
            padding: 30px;
            overflow-y: auto;
            background: #0d1117;
            scroll-behavior: smooth;
        }

        /* Masquer la scrollbar */
        .chat-container::-webkit-scrollbar {
            width: 0px;
            background: transparent;
        }

        .message {
            margin-bottom: 20px;
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message-user {
            display: flex;
            justify-content: flex-end;
        }

        .message-bot {
            display: flex;
            justify-content: flex-start;
        }

        .message-system {
            text-align: center;
            color: #ffa657;
            font-style: italic;
            font-size: 0.9em;
            margin: 10px 0;
        }

        .message-content {
            max-width: 70%;
            padding: 15px 20px;
            border-radius: 15px;
            word-wrap: break-word;
            position: relative;
        }

        .message-user .message-content {
            background: linear-gradient(135deg, #1f6feb 0%, #58a6ff 100%);
            color: white;
            border-bottom-right-radius: 5px;
        }

        .message-bot .message-content {
            background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
            color: white;
            border-bottom-left-radius: 5px;
        }

        .message-label {
            font-size: 0.85em;
            font-weight: bold;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .input-container {
            background: #161b22;
            padding: 25px 30px;
            border-top: 2px solid #30363d;
            display: flex;
            gap: 15px;
        }

        #messageInput {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #30363d;
            border-radius: 25px;
            background: #0d1117;
            color: #c9d1d9;
            font-size: 1em;
            outline: none;
            transition: all 0.3s ease;
        }

        #messageInput:focus {
            border-color: #58a6ff;
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1);
        }

        #sendButton {
            padding: 15px 35px;
            background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(46, 160, 67, 0.3);
        }

        #sendButton:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(46, 160, 67, 0.4);
        }

        #sendButton:disabled {
            background: #30363d;
            cursor: not-allowed;
            box-shadow: none;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 10px;
            color: #8b949e;
        }

        .loading.active {
            display: block;
        }

        .loading-dots {
            display: inline-block;
        }

        .loading-dots span {
            animation: blink 1.4s infinite;
            animation-fill-mode: both;
            margin: 0 2px;
        }

        .loading-dots span:nth-child(2) {
            animation-delay: 0.2s;
        }

        .loading-dots span:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes blink {
            0%, 80%, 100% {
                opacity: 0;
            }
            40% {
                opacity: 1;
            }
        }

        .status {
            text-align: center;
            padding: 10px;
            background: #161b22;
            color: #8b949e;
            font-size: 0.9em;
            border-top: 1px solid #30363d;
        }

        @media (max-width: 768px) {
            .container {
                height: 100vh;
                border-radius: 0;
            }

            .header h1 {
                font-size: 1.8em;
            }

            .message-content {
                max-width: 85%;
            }

            .input-container {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Chat'bruti</h1>
            <p>Mode: Réponses WTF activées 🔥</p>
        </div>

        <div class="chat-container" id="chatContainer">
            <div class="message-system">🎉 Bienvenue sur Chat'bruti!</div>
            <div class="message-system">💬 Posez une question pour obtenir une réponse délirante</div>
        </div>

        <div class="loading" id="loading">
            <span class="loading-dots">
                🤔 Chat'bruti réfléchit<span>.</span><span>.</span><span>.</span>
            </span>
        </div>

        <div class="input-container">
            <input 
                type="text" 
                id="messageInput" 
                placeholder="Tapez votre message ici..."
                autocomplete="off"
            >
            <button id="sendButton">Envoyer 🚀</button>
        </div>

        <div class="status" id="status">
            💡 Prêt à recevoir vos questions WTF
        </div>
    </div>

    <script>
        const chatContainer = document.getElementById('chatContainer');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const loading = document.getElementById('loading');
        const status = document.getElementById('status');

        messageInput.focus();

        function addMessage(text, type) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message message-${type}`;

            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';

            if (type === 'user') {
                contentDiv.innerHTML = `<div class="message-label">Vous</div>${text}`;
            } else if (type === 'bot') {
                contentDiv.innerHTML = `<div class="message-label">Chat'bruti</div>${text}`;
            }

            messageDiv.appendChild(contentDiv);
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            // Désactiver l'envoi
            messageInput.disabled = true;
            sendButton.disabled = true;
            loading.classList.add('active');
            status.textContent = '🤔 Chatbruti réfléchit...';

            // Afficher le message utilisateur
            addMessage(message, 'user');
            messageInput.value = '';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();

                if (data.response) {
                    addMessage(data.response, 'bot');
                    status.textContent = '💡 Prêt à recevoir vos questions WTF';
                } else {
                    addMessage('❌ Erreur: Pas de réponse', 'bot');
                    status.textContent = '❌ Erreur lors de la génération';
                }
            } catch (error) {
                addMessage(`❌ Erreur: ${error.message}`, 'bot');
                status.textContent = '❌ Erreur de connexion';
            } finally {
                // Réactiver l'envoi
                messageInput.disabled = false;
                sendButton.disabled = false;
                loading.classList.remove('active');
                messageInput.focus();
            }
        }

        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message vide'}), 400
        
        # Générer la réponse
        response = chatbot.generer_reponse_idiote(user_message)
        
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("🚀 Serveur Gemma Chatbot démarré!")
    print("="*60)
    print("📍 Accédez au chatbot sur: http://localhost:5000")
    print("⚡ Appuyez sur Ctrl+C pour arrêter le serveur")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=2000)