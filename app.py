import os
from flask import Flask, request
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
            ip VARCHAR(45),
            country VARCHAR(100),
            device VARCHAR(255),
            time TIMESTAMPTZ DEFAULT NOW()
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def log_visit():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO visits (ip, country, device, time) VALUES (%s, %s, %s, %s)',
        (
            request.remote_addr,
            request.headers.get('CF-IPCountry', 'unknown'),
            request.headers.get('User-Agent', 'unknown'),
            datetime.now(timezone.utc)
        )
    )
    conn.commit()
    cur.close()
    conn.close()

@app.route('/api/v1/status')
def status():
    log_visit()
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
