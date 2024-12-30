import tkinter as tk
from tkinter import messagebox
from sql import checkKey
import requests
from gui import BotGUI

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login - KeyDrop Bot")
        self.root.geometry("400x200")
        self.root.configure(bg="#2C2F33")
        self.root.resizable(False, False)

        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        x = (screenWidth - 400) // 2
        y = (screenHeight - 200) // 2
        self.root.geometry(f"400x200+{x}+{y}")

        mainFrame = tk.Frame(self.root, bg="#2C2F33", padx=20, pady=20)
        mainFrame.pack(expand=True)

        keyLabel = tk.Label(
            mainFrame,
            text="Escreva seu código aqui",
            font=("Helvetica", 12),
            fg="#FFFFFF",
            bg="#2C2F33"
        )
        keyLabel.pack(pady=(0, 5))

        self.keyInput = tk.Entry(
            mainFrame,
            width=30,
            font=("Helvetica", 11),
            bg="#23272A",
            fg="white",
            insertbackground="white"
        )
        
        try:
            with open('key.belbot', 'r') as f:
                savedKey = f.read().strip()
                self.keyInput.insert(0, savedKey)
        except:
            self.keyInput.insert(0, "Digite sua chave de acesso")
            
        self.keyInput.pack(pady=20)

        self.confirmButton = tk.Button(
            mainFrame,
            text="Confirmar",
            command=self.validateKey,
            bg="#43B581",
            fg="white",
            activebackground="#3CA374",
            font=("Helvetica", 12),
            width=15,
            height=1,
            border=0,
            cursor="hand2"
        )
        self.confirmButton.pack(pady=10)

    def getUserIp(self):
        try:
            response = requests.get('https://api.ipify.org?format=json')
            return response.json()['ip']
        except:
            return None

    def validateKey(self):
        key = self.keyInput.get().strip()
        if not key:
            messagebox.showwarning("Erro", "Por favor, digite uma chave")
            return
            
        result = checkKey(key)
        if result["status"]:
            try:
                with open('key.belbot', 'w') as f:
                    f.write(key)
            except Exception as e:
                messagebox.showwarning("Erro", "Não foi possível salvar a chave")
                return
                
            self.root.destroy()
            bot_gui = BotGUI()
            bot_gui.run()
        else:
            messagebox.showwarning("Erro", result["message"])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    app.run()