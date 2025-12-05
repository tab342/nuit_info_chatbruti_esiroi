import tkinter as tk
from tkinter import scrolledtext
from functools import partial
from test import ChatbotGemma  # Assumes your code is saved as chatbot.py

class ChatbotGUI:
    def __init__(self):
        self.bot = ChatbotGemma(model_name="gemma3:1b")

        self.root = tk.Tk()
        self.root.title("Chatbot Gemma - Interface Graphique")
        self.root.geometry("650x600")
        self.root.configure(bg="#1e1e1e")

        # Zone d'affichage du chat
        self.chat_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=25, bg="#2b2b2b", fg="white", font=("Arial", 12))
        self.chat_box.pack(pady=10)
        self.chat_box.config(state=tk.DISABLED)

        # Champ de saisie utilisateur
        self.entry = tk.Entry(self.root, width=70, bg="#2b2b2b", fg="white", font=("Arial", 12))
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.send_message)

        # Bouton d'envoi
        self.button = tk.Button(self.root, text="Envoyer", command=self.send_message, bg="#444", fg="white", font=("Arial", 12))
        self.button.pack(pady=5)

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        self.entry.delete(0, tk.END)
        self.display_message(f"Vous: {user_input}\n")

        # Génération réponse
        self.display_message("Gemma réfléchit...\n")
        response = self.bot.generer_reponse(user_input)
        self.display_message(f"Gemma: {response}\n\n")

    def display_message(self, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, message)
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.see(tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = ChatbotGUI()
    gui.run()
