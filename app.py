import os
from flask import Flask
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = Flask(__name__)

def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

@app.route('/api/v1/status')
def status():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
