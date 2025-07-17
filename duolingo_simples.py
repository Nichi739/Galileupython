import tkinter as tk
from tkinter import messagebox
import random

# Dicionário grande de palavras (você pode aumentar quanto quiser)
dicionario = {
    "Dog": "cachorro",
    "Cat": "gato",
    "Apple": "maçã",
    "House": "casa",
    "Water": "água",
    "Book": "livro",
    "Chair": "cadeira",
    "Table": "mesa",
    "Pen": "caneta",
    "Window": "janela",
    "Car": "carro",
    "Sun": "sol",
    "Moon": "lua",
    "Star": "estrela",
    "Phone": "telefone",
    "Computer": "computador",
    "Tree": "árvore",
    "Fish": "peixe",
    "Bird": "pássaro",
    "Mountain": "montanha"
}

class DuolingoInfinito:
    def __init__(self, root):
        self.root = root
        self.root.title("🦉 Duolingo Infinito")
        self.root.geometry("400x300")
        self.score = 0
        self.total = 0

        self.label_title = tk.Label(root, text="Traduza do inglês para o português", font=("Arial", 14))
        self.label_title.pack(pady=10)

        self.label_pergunta = tk.Label(root, text="", font=("Arial", 24))
        self.label_pergunta.pack(pady=20)

        self.entry_resposta = tk.Entry(root, font=("Arial", 16))
        self.entry_resposta.pack()

        self.button_verificar = tk.Button(root, text="Verificar", command=self.verificar_resposta)
        self.button_verificar.pack(pady=10)

        self.label_resultado = tk.Label(root, text="", font=("Arial", 14))
        self.label_resultado.pack(pady=5)

        self.button_sair = tk.Button(root, text="Sair do jogo", command=self.finalizar_jogo)
        self.button_sair.pack(pady=5)

        self.sortear_palavra()

    def sortear_palavra(self):
        self.palavra_atual, self.resposta_certa = random.choice(list(dicionario.items()))
        self.label_pergunta.config(text=self.palavra_atual)
        self.entry_resposta.delete(0, tk.END)
        self.label_resultado.config(text="")

    def verificar_resposta(self):
        resposta_usuario = self.entry_resposta.get().strip().lower()
        self.total += 1

        if resposta_usuario == self.resposta_certa.lower():
            self.score += 1
            self.label_resultado.config(text="✅ Correto!", fg="green")
        else:
            self.label_resultado.config(
                text=f"❌ Errado. Resposta certa: {self.resposta_certa}", fg="red"
            )

        self.root.after(1500, self.sortear_palavra)

    def finalizar_jogo(self):
        messagebox.showinfo("Fim do Jogo", f"Você acertou {self.score} de {self.total} tentativas.")
        self.root.quit()

# Iniciar o jogo
if __name__ == "__main__":
    root = tk.Tk()
    jogo = DuolingoInfinito(root)
    root.mainloop()
