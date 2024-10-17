import tkinter as tk
from tkinter import ttk, messagebox
from mission_form import MissionForm
from database.database import Database

class MissionList(tk.Frame):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "Data", "Destino", "Estado"))
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Data", text="Data de Lançamento")
        self.tree.heading("Destino", text="Destino")
        self.tree.heading("Estado", text="Estado da Missão")
        self.tree.pack()

        self.btn_add = tk.Button(self, text="Adicionar Missão", command=self.add_missao)
        self.btn_add.pack()

        self.btn_edit = tk.Button(self, text="Editar Missão", command=self.edit_missao)
        self.btn_edit.pack()

        self.btn_delete = tk.Button(self, text="Excluir Missão", command=self.delete_missao)
        self.btn_delete.pack()

        self.load_missoes()

    def load_missoes(self):
        try:
            for row in self.db.get_missoes():
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar missões: {e}")

    def add_missao(self):
        try:
            MissionForm(self.master, self.db)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir formulário de missão: {e}")

    def edit_missao(self):
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                raise ValueError("Nenhuma missão selecionada.")
            missao_id = self.tree.item(selected_item[0])['values'][0]
            missao = self.db.get_missao_by_id(missao_id)
            if missao:
                MissionForm(self.master, self.db, missao)
            else:
                raise ValueError(f"Missão com ID {missao_id} não encontrada.")
        except ValueError as e:
            messagebox.showwarning("Aviso", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar missão: {e}")

    def delete_missao(self):
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                raise ValueError("Nenhuma missão selecionada.")
            missao_id = self.tree.item(selected_item[0])['values'][0]
            confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir a missão {missao_id}?")
            if confirm:
                self.db.delete_missao(missao_id)
                self.load_missoes()
        except ValueError as e:
            messagebox.showwarning("Aviso", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir missão: {e}")
