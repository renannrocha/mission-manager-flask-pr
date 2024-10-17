import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_name="expedicoes_espaciais.db"):
        try:
            self.conn = sqlite3.connect(db_name)
            self.create_table()
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
    
    def create_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS missao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data_lancamento TEXT NOT NULL,
                destino TEXT NOT NULL,
                estado_missao TEXT NOT NULL,
                tripulacao TEXT,
                carga_util TEXT,
                duracao TEXT,
                custo REAL,
                status TEXT
            )
            """
            self.conn.execute(query)
            self.conn.commit()
        except Error as e:
            print(f"Erro ao criar a tabela: {e}")

    def add_missao(self, missao):
        try:
            query = """
            INSERT INTO missao (nome, data_lancamento, destino, estado_missao, tripulacao, carga_util, duracao, custo, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.conn.execute(query, missao)
            self.conn.commit()
        except Error as e:
            print(f"Erro ao adicionar missão: {e}")

    def get_missoes(self):
        try:
            cursor = self.conn.execute("SELECT * FROM missao")
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao recuperar missões: {e}")
            return []

    def get_missao_by_id(self, missao_id):
        try:
            cursor = self.conn.execute("SELECT * FROM missao WHERE id = ?", (missao_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Erro ao recuperar missão pelo ID {missao_id}: {e}")
            return None

    def update_missao(self, missao_id, updated_data):
        try:
            query = """
            UPDATE missao SET nome = ?, data_lancamento = ?, destino = ?, estado_missao = ?, tripulacao = ?, carga_util = ?, duracao = ?, custo = ?, status = ?
            WHERE id = ?
            """
            self.conn.execute(query, (*updated_data, missao_id))
            self.conn.commit()
        except Error as e:
            print(f"Erro ao atualizar missão com ID {missao_id}: {e}")

    def delete_missao(self, missao_id):
        try:
            self.conn.execute("DELETE FROM missao WHERE id = ?", (missao_id,))
            self.conn.commit()
        except Error as e:
            print(f"Erro ao excluir missão com ID {missao_id}: {e}")
