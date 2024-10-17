import tkinter as tk
from gui.mission_list import MissionList
from database.database import Database
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        try:
            self.title("Sistema de Expedições Espaciais")
            self.geometry("600x400")

            self.db = Database()
            self.mission_list = MissionList(self, self.db)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar a aplicação: {e}")

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Erro fatal: {e}")
