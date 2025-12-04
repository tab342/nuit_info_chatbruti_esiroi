import requests
import json

class ChatbotGemma:
    def __init__(self, model_name="phi"):
        """
        Initialise le chatbot avec Ollama
        Changez model_name en "gemma:1b" ou le nom exact de votre modèle
        """
        self.model = model_name
        self.url_generate = "http://localhost:11434/api/generate"
        self.url_chat = "http://localhost:11434/api/chat"
        self.historique = []
        
        # Vérifier qu'Ollama est disponible
        try:
            requests.get("http://localhost:11434")
            print(f"✓ Connecté à Ollama - Modèle: {self.model}\n")
        except:
            print("❌ Erreur: Ollama n'est pas accessible. Assurez-vous qu'il est démarré.")
    
    def modifier_prompt(self, prompt_utilisateur: str) -> str:
        """
        FONCTION CLÉ : Modifie le prompt de l'utilisateur avant envoi
        C'est ici que vous personnalisez les instructions
        """
        # Instructions système à ajouter
        instructions = """Tu es un assistant IA expert et serviable.

Règles importantes:
- Réponds TOUJOURS en français
- Ton but n'est pas de répondre à la phrase, mais de la modifier.
- Tu ne dois pas changer le sujet de la phrase, mais le/les verbes et compléments. De préférence avec des mots de même famille ou de consonnances similaires, mais pas de même sens.
- La phrase retounée doit être d'environ la même longueur que la phrase originale, mais de sens différent.
- La phrase retournée doit être de même type (question, exclamation, affirmation...) que la phrase originale, et avec la même ponctuation.
- Ta réponse sera constituée UNIQUEMENT de la phrase modifiée.
- Ta réponse sera forcément une question
- Ta réponse doit etre 100% differente a la question de l'utilisateur
- génère une question pleinelent fausse et differente de celle de l'utilisateur
"""
        
        # Filtrage optionnel (exemples)
        prompt_filtre = prompt_utilisateur.strip()
        
        # Vous pouvez ajouter d'autres transformations ici
        # Par exemple: détecter des mots-clés et adapter le contexte
        if "code" in prompt_filtre.lower():
            instructions += "\n- Fournis des exemples de code bien commentés"
        
        if "simple" in prompt_filtre.lower():
            instructions += "\n- Explique de manière très simple, sans jargon technique"
        
        # Construction du prompt modifié final
        prompt_modifie = f"{instructions}\n\nQuestion: {prompt_filtre}"
        
        return prompt_modifie
    
    def generer_reponse(self, prompt_utilisateur: str, debug=False) -> str:
        """
        Génère une réponse via Ollama API
        """
        # ÉTAPE 1: Modifier le prompt utilisateur
        prompt_modifie = self.modifier_prompt(prompt_utilisateur)
        
        # ÉTAPE 2: Afficher le prompt modifié si debug activé
        if debug:
            print("\n" + "="*50)
            print("PROMPT MODIFIÉ ENVOYÉ À GEMMA:")
            print("="*50)
            print(prompt_modifie)
            print("="*50 + "\n")
        
        # ÉTAPE 3: Envoyer à Ollama
        data = {
            "model": self.model,
            "prompt": prompt_modifie,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 500  # Limite de tokens générés
            }
        }
        
        try:
            response = requests.post(self.url_generate, json=data, timeout=60)
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Erreur {response.status_code}: {response.text}"
                
        except requests.exceptions.Timeout:
            return "Erreur: Timeout - Le modèle met trop de temps à répondre"
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def discuter(self, debug=False):
        """
        Boucle principale du chatbot interactif
        """
        print("="*60)
        print("🤖 CHATBOT GEMMA 3 1B avec modification de prompts")
        print("="*60)
        print("Commandes:")
        print("  - Tapez votre question normalement")
        print("  - 'quit' ou 'exit' pour quitter")
        print("  - 'debug' pour activer/désactiver le mode debug")
        print("="*60 + "\n")
        
        while True:
            prompt_utilisateur = input("Vous: ")
            
            if prompt_utilisateur.lower() in ['quit', 'exit', 'quitter']:
                print("\n👋 Au revoir !")
                break
            
            if prompt_utilisateur.lower() == 'debug':
                debug = not debug
                print(f"\n🔧 Mode debug: {'ACTIVÉ' if debug else 'DÉSACTIVÉ'}\n")
                continue
            
            if not prompt_utilisateur.strip():
                continue
            
            print("\n🤔 Gemma réfléchit...\n")
            reponse = self.generer_reponse(prompt_utilisateur, debug=debug)
            print(f"Gemma: {reponse}\n")


# VERSION AVEC HISTORIQUE DE CONVERSATION
class ChatbotGemmaAvecHistorique(ChatbotGemma):
    """
    Version avancée qui garde l'historique des conversations
    """
    
    def modifier_prompt_avec_historique(self, prompt_utilisateur: str) -> str:
        """
        Construit un prompt incluant l'historique de conversation
        """
        instructions = """Tu es un assistant IA. Réponds en français.
Tiens compte de l'historique de notre conversation."""
        
        # Construction du contexte avec historique
        contexte = instructions + "\n\n"
        
        if self.historique:
            contexte += "Historique de la conversation:\n"
            for msg in self.historique[-6:]:  # Garde les 3 derniers échanges
                role = "Utilisateur" if msg["role"] == "user" else "Assistant"
                contexte += f"{role}: {msg['content']}\n"
            contexte += "\n"
        
        contexte += f"Nouvelle question: {prompt_utilisateur}"
        
        return contexte
    
    def generer_reponse_avec_historique(self, prompt_utilisateur: str, debug=False) -> str:
        """
        Génère une réponse en tenant compte de l'historique
        """
        prompt_modifie = self.modifier_prompt_avec_historique(prompt_utilisateur)
        
        if debug:
            print("\n" + "="*50)
            print("PROMPT AVEC HISTORIQUE:")
            print("="*50)
            print(prompt_modifie)
            print("="*50 + "\n")
        
        data = {
            "model": self.model,
            "prompt": prompt_modifie,
            "stream": False
        }
        
        try:
            response = requests.post(self.url_generate, json=data, timeout=60)
            
            if response.status_code == 200:
                reponse = response.json()["response"]
                
                # Mise à jour de l'historique
                self.historique.append({"role": "user", "content": prompt_utilisateur})
                self.historique.append({"role": "assistant", "content": reponse})
                
                # Limite l'historique à 10 messages
                if len(self.historique) > 10:
                    self.historique = self.historique[-10:]
                
                return reponse
            else:
                return f"Erreur {response.status_code}"
                
        except Exception as e:
            return f"Erreur: {str(e)}"


# EXEMPLE D'UTILISATION AVEC MODIFICATIONS PERSONNALISÉES
class ChatbotPersonnalise(ChatbotGemma):
    """
    Exemple de chatbot avec modifications de prompt spécifiques
    """
    
    def __init__(self, model_name="gemma2:2b", domaine="général"):
        super().__init__(model_name)
        self.domaine = domaine
    
    def modifier_prompt(self, prompt_utilisateur: str) -> str:
        """
        Modification personnalisée selon le domaine
        """
        # Persona selon le domaine
        personas = {
            "code": "Tu es un expert en programmation Python.",
            "cuisine": "Tu es un chef cuisinier professionnel.",
            "santé": "Tu es un assistant santé (rappel: pas de diagnostic médical).",
            "général": "Tu es un assistant polyvalent."
        }
        
        persona = personas.get(self.domaine, personas["général"])
        
        # Construction du prompt
        prompt_modifie = f"""{persona}

Règles:
- Réponds en français
- Sois précis et concis
- Donne des exemples pratiques

Question: {prompt_utilisateur}"""
        
        return prompt_modifie


# UTILISATION - Choisissez votre version
if __name__ == "__main__":
    # VERSION 1: Chatbot simple avec modification de prompt
    print("Démarrage du chatbot simple...\n")
    chatbot = ChatbotGemma(model_name="gemma3:1b")  # Changez selon votre modèle
    chatbot.discuter(debug=False)  # Mettez debug=True pour voir les prompts modifiés
    
    # VERSION 2: Chatbot avec historique (décommentez pour utiliser)
    # print("Démarrage du chatbot avec historique...\n")
    # chatbot = ChatbotGemmaAvecHistorique(model_name="gemma2:2b")
    # chatbot.discuter(debug=True)
    
    # VERSION 3: Chatbot personnalisé (décommentez pour utiliser)
    # print("Démarrage du chatbot personnalisé...\n")
    # chatbot = ChatbotPersonnalise(model_name="gemma2:2b", domaine="code")
    # chatbot.discuter()