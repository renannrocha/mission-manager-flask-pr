import tkinter as tk
from tkinter import messagebox
from database.database import Database

class MissionForm(tk.Toplevel):
    def __init__(self, master, db, missao=None):
        super().__init__(master)
        self.db = db
        self.missao = missao
        self.title("Formulário de Missão")
        self.geometry("400x400")

        self.create_widgets()

        if self.missao:
            self.load_missao_data()

    def create_widgets(self):
        self.lbl_nome = tk.Label(self, text="Nome da Missão")
        self.lbl_nome.pack()
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack()

        self.lbl_data = tk.Label(self, text="Data de Lançamento")
        self.lbl_data.pack()
        self.entry_data = tk.Entry(self)
        self.entry_data.pack()

        self.lbl_destino = tk.Label(self, text="Destino")
        self.lbl_destino.pack()
        self.entry_destino = tk.Entry(self)
        self.entry_destino.pack()

        self.lbl_estado = tk.Label(self, text="Estado da Missão")
        self.lbl_estado.pack()
        self.entry_estado = tk.Entry(self)
        self.entry_estado.pack()

        self.btn_save = tk.Button(self, text="Salvar", command=self.save_missao)
        self.btn_save.pack()

    def load_missao_data(self):
        try:
            self.entry_nome.insert(0, self.missao[1])
            self.entry_data.insert(0, self.missao[2])
            self.entry_destino.insert(0, self.missao[3])
            self.entry_estado.insert(0, self.missao[4])
        except IndexError as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados da missão: {e}")

    def save_missao(self):
        try:
            nome = self.entry_nome.get()
            data = self.entry_data.get()
            destino = self.entry_destino.get()
            estado = self.entry_estado.get()

            if not nome or not data or not destino or not estado:
                raise ValueError("Todos os campos são obrigatórios.")

            if self.missao:
                self.db.update_missao(self.missao[0], (nome, data, destino, estado, "", "", "", 0, ""))
            else:
                self.db.add_missao((nome, data, destino, estado, "", "", "", 0, ""))

            messagebox.showinfo("Info", "Missão salva com sucesso!")
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar missão: {e}")
