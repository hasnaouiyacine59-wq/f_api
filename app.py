import os
from flask import Flask, jsonify
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = Flask(__name__)

def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def init_db():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS visits (ip VARCHAR(45) UNIQUE)')

@app.route('/api/v1/<ip>')
def status(ip):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT 1 FROM visits WHERE ip = %s', (ip,))
            if cur.fetchone():
                return jsonify({'message': 'yes'}), 200
            cur.execute('INSERT INTO visits (ip) VALUES (%s)', (ip,))
    return jsonify({'message': 'no'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
