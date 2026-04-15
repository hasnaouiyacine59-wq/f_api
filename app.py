import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import psycopg2
from datetime import datetime, timezone

load_dotenv()

app = Flask(__name__)

def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            ip VARCHAR(45) UNIQUE,
            country VARCHAR(100),
            device VARCHAR(255),
            time TIMESTAMPTZ
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/api/v1/status', methods=['POST'])
def status():
    data = request.get_json()
    ip = data.get('ip')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT 1 FROM visits WHERE ip = %s', (ip,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'message': 'exist'}), 200
    cur.execute(
        'INSERT INTO visits (ip, country, device, time) VALUES (%s, %s, %s, %s)',
        (ip, data.get('country'), data.get('device'), data.get('time', datetime.now(timezone.utc)))
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'ok'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
