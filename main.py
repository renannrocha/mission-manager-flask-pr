from src.app import app
from src.database import db

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
