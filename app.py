import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import psycopg2
import json

load_dotenv()

app = Flask(__name__)

def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def init_db():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS visits (
                    ip VARCHAR(45) UNIQUE,
                    country VARCHAR(100),
                    cc VARCHAR(10),
                    city VARCHAR(100),
                    locale VARCHAR(20),
                    timezone VARCHAR(100),
                    os VARCHAR(50),
                    "window" JSONB,
                    titles JSONB,
                    iframes JSONB,
                    iframe0_attrs JSONB,
                    iframe0_alts JSONB
                )
            ''')

@app.route('/api/v1/<ip>')
def check_ip(ip):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT 1 FROM visits WHERE ip = %s', (ip,))
            if cur.fetchone():
                return jsonify({'used': 'yes'}), 200
    return jsonify({'used': 'no'}), 200

@app.route('/api/v1/status', methods=['POST'])
def status():
    d = request.get_json()
    ip = d.get('ip')
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT 1 FROM visits WHERE ip = %s', (ip,))
            if cur.fetchone():
                return jsonify({'used': 'yes'}), 200
            cur.execute('''
                INSERT INTO visits (ip, country, cc, city, locale, timezone, os, "window", titles, iframes, iframe0_attrs, iframe0_alts)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''', (
                ip, d.get('country'), d.get('cc'), d.get('city'),
                d.get('locale'), d.get('timezone'), d.get('os'),
                json.dumps(d.get('window')), json.dumps(d.get('titles')),
                json.dumps(d.get('iframes')), json.dumps(d.get('iframe0_attrs')),
                json.dumps(d.get('iframe0_alts'))
            ))
    return jsonify({'used': 'no'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
