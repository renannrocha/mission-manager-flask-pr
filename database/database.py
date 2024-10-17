import sqlite3

DB_NAME = "expedicoes_espaciais.db"

def get_db_connection():
    """Obtém uma conexão com o banco de dados."""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def execute_query(query, params=()):
    """Executa uma query no banco de dados."""
    conn = get_db_connection()
    if conn is None:
        print("Conexão não estabelecida. Query não executada.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao executar a query: {e}")
    finally:
        conn.close()

def search_query(query, params=()):
    """Busca dados no banco de dados e retorna os resultados."""
    conn = get_db_connection()
    if conn is None:
        print("Conexão não estabelecida. Busca não realizada.")
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Erro ao buscar dados: {e}")
        return []
    finally:
        conn.close()

def init_db():
    """Inicializa o banco de dados criando as tabelas necessárias."""
    conn = get_db_connection()
    if conn is None:
        print("Conexão não estabelecida. Banco de dados não inicializado.")
        return

    try:
        cursor = conn.cursor()
        
        cursor.execute('''
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
        ''')

        conn.commit()
        print("Banco de dados e tabela 'missao' criados com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        conn.close()

# Funções CRUD específicas para o sistema de expedições

def adicionar_missao(nome, data_lancamento, destino, estado_missao, tripulacao, carga_util, duracao, custo, status):
    """Adiciona uma nova missão ao banco de dados."""
    query = '''
        INSERT INTO missao (nome, data_lancamento, destino, estado_missao, tripulacao, carga_util, duracao, custo, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    execute_query(query, (nome, data_lancamento, destino, estado_missao, tripulacao, carga_util, duracao, custo, status))

def atualizar_missao(missao_id, nome, data_lancamento, destino, estado_missao, tripulacao, carga_util, duracao, custo, status):
    """Atualiza os dados de uma missão existente."""
    query = '''
        UPDATE missao
        SET nome = ?, data_lancamento = ?, destino = ?, estado_missao = ?, tripulacao = ?, carga_util = ?, duracao = ?, custo = ?, status = ?
        WHERE id = ?
    '''
    execute_query(query, (nome, data_lancamento, destino, estado_missao, tripulacao, carga_util, duracao, custo, status, missao_id))

def excluir_missao(missao_id):
    """Exclui uma missão do banco de dados."""
    query = "DELETE FROM missao WHERE id = ?"
    execute_query(query, (missao_id,))

def listar_missoes():
    """Retorna uma lista de todas as missões registradas no banco de dados."""
    query = "SELECT * FROM missao"
    return search_query(query)

def buscar_missao_por_id(missao_id):
    """Busca os detalhes de uma missão pelo ID."""
    query = "SELECT * FROM missao WHERE id = ?"
    return search_query(query, (missao_id,))

def buscar_missoes_por_data(data_inicio, data_fim):
    """Busca missões lançadas dentro de um intervalo de datas."""
    query = '''
        SELECT * FROM missao
        WHERE data_lancamento BETWEEN ? AND ?
    '''
    return search_query(query, (data_inicio, data_fim))

if __name__ == "__main__":
    init_db()
