import tkinter as tk
from tkinter import ttk
from bot import execute, stop_bot
import threading

class BotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KeyDrop Bot")
        self.root.geometry("400x500")
        self.root.configure(bg="#2C2F33")
        self.root.resizable(False, False)

        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        x = (screenWidth - 400) // 2
        y = (screenHeight - 500) // 2
        self.root.geometry(f"400x500+{x}+{y}")

        main = tk.Frame(self.root, bg="#2C2F33", padx=20, pady=20)
        main.pack(fill="both", expand=True)

        title = tk.Label(
            main,
            text="KeyDrop Bot",
            font=("Helvetica", 24, "bold"),
            fg="#FFFFFF",
            bg="#2C2F33"
        )
        title.pack(pady=20)

        selectBox = tk.Frame(main, bg="#2C2F33")
        selectBox.pack(pady=10)

        selectLabel = tk.Label(
            selectBox,
            text="Qual sorteio você quer participar:",
            font=("Helvetica", 12),
            fg="#FFFFFF",
            bg="#2C2F33"
        )
        selectLabel.pack(pady=(0, 5))

        style = ttk.Style()
        style.theme_create("custom", parent="alt", settings={
            "TCombobox": {
                "configure": {
                    "selectbackground": "#23272A",
                    "selectforeground": "white",
                    "fieldbackground": "#23272A",
                    "background": "#2C2F33",
                    "foreground": "white",
                    "padding": 5,
                    "arrowsize": 15
                }
            }
        })
        style.theme_use("custom")

        self.nivel = tk.StringVar()
        self.nivelSelect = ttk.Combobox(
            selectBox,
            textvariable=self.nivel,
            values=["AMATEUR", "CONTENDER", "LEGEND", "CHALLENGER", "CHAMPION"],
            state="readonly",
            width=25,
            font=("Helvetica", 11)
        )
        self.nivelSelect.set("AMATEUR")
        self.nivelSelect.pack(pady=5)

        self.root.option_add('*TCombobox*Listbox.background', '#23272A')
        self.root.option_add('*TCombobox*Listbox.foreground', 'white')
        self.root.option_add('*TCombobox*Listbox.selectBackground', '#7289DA')
        self.root.option_add('*TCombobox*Listbox.selectForeground', 'white')

        valorFrame = tk.Frame(main, bg="#2C2F33")
        valorFrame.pack(pady=10)

        valorLabel = tk.Label(
            valorFrame,
            text="Valor mínimo:",
            font=("Helvetica", 12),
            fg="#FFFFFF",
            bg="#2C2F33"
        )
        valorLabel.pack(pady=(0, 5))

        def validateFloat(text):
            if text == "" or text == "0" or text == "0.": 
                return True
            try:
                if '.' not in text:
                    float(text)
                    return True
                partes = text.split('.')
                if len(partes) > 2:
                    return False
                if len(partes[1]) <= 2:
                    float(text)
                    return True
                return False
            except:
                return False

        vcmd = (self.root.register(validateFloat), '%P')

        self.valorEntry = tk.Entry(
            valorFrame,
            validate='key',
            validatecommand=vcmd,
            width=10,
            font=("Helvetica", 11),
            bg="#23272A",
            fg="white",
            insertbackground="white",
            justify="center"
        )
        self.valorEntry.insert(0, "0.00")
        self.valorEntry.pack(pady=5)

        def formatValue(event):
            try:
                valor = self.valorEntry.get()
                if (valor == "" or valor == "."):
                    self.valorEntry.delete(0, tk.END)
                    self.valorEntry.insert(0, "0.00")
                else:
                    valor = float(valor)
                    self.valorEntry.delete(0, tk.END)
                    self.valorEntry.insert(0, f"{valor:.2f}")
            except:
                self.valorEntry.delete(0, tk.END)
                self.valorEntry.insert(0, "0.00")

        self.valorEntry.bind('<FocusOut>', formatValue)

        buttonFrame = tk.Frame(main, bg="#2C2F33")
        buttonFrame.pack(pady=20)

        buttonStyle = {
            "font": ("Helvetica", 12),
            "width": 15,
            "height": 2,
            "border": 0,
            "cursor": "hand2"
        }

        self.startButton = tk.Button(
            buttonFrame,
            text="Iniciar Bot",
            command=self.startBot,
            bg="#43B581",
            fg="white",
            activebackground="#3CA374",
            **buttonStyle
        )
        self.startButton.pack(pady=10)

        self.stopButton = tk.Button(
            buttonFrame,
            text="Encerrar",
            command=self.encerrarPrograma,
            bg="#F04747",
            fg="white",
            activebackground="#D84040",
            **buttonStyle
        )
        self.stopButton.pack(pady=10)

        statusFrame = tk.Frame(main, bg="#2C2F33", pady=20)
        statusFrame.pack(fill="x")

        self.statusLabel = tk.Label(
            statusFrame,
            text="Status: Bot parado",
            font=("Helvetica", 12),
            fg="#FFFFFF",
            bg="#23272A",
            padx=20,
            pady=10
        )
        self.statusLabel.pack(fill="x")

        infoText = "Desenvolvido por Honn3x\nVersão 1.0"
        infoLabel = tk.Label(
            main,
            text=infoText,
            font=("Helvetica", 8),
            fg="#99AAB5",
            bg="#2C2F33"
        )
        infoLabel.pack(side="bottom", pady=20)

    def startBot(self):
        tipoSorteio = self.nivel.get()
        try:
            valorMinimo = float(self.valorEntry.get())
        except ValueError:
            valorMinimo = 0.0

        self.nivelSelect.config(state="disabled")
        self.valorEntry.config(state="disabled")
        
        self.startButton.config(state="disabled")
        self.stopButton.config(state="normal")
        self.statusLabel.config(
            text="Status: Bot em execução",
            fg="#43B581"
        )

        thread = threading.Thread(target=lambda: execute(tipoSorteio, valorMinimo))
        thread.daemon = True
        thread.start()

    def pararBot(self):
        self.nivelSelect.config(state="readonly")
        self.valorEntry.config(state="normal")
        
        self.startButton.config(state="normal")
        self.stopButton.config(state="disabled")
        self.statusLabel.config(
            text="Status: Bot parado",
            fg="#F04747"
        )
        stop_bot()

    def encerrarPrograma(self):
        stop_bot()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BotGUI()
    app.run()