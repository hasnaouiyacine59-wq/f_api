import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = Flask(__name__)

def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS visits (ip VARCHAR(45) UNIQUE)')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/api/v1/status', methods=['POST'])
def status():
    ip = request.get_json().get('ip')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT 1 FROM visits WHERE ip = %s', (ip,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'message': 'exist'}), 200
    cur.execute('INSERT INTO visits (ip) VALUES (%s)', (ip,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'ok'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
