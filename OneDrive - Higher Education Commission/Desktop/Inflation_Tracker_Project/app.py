from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'inflation_tracker.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/items')
def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM monthly_prices').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in items])

@app.route('/api/stats')
def get_stats():
    conn = get_db_connection()
    # Top 5 highest increases
    increases = conn.execute('SELECT item_name, change_nov_25_oct_25 FROM monthly_prices ORDER BY change_nov_25_oct_25 DESC LIMIT 5').fetchall()
    # Top 5 decreases
    decreases = conn.execute('SELECT item_name, change_nov_25_oct_25 FROM monthly_prices ORDER BY change_nov_25_oct_25 ASC LIMIT 5').fetchall()
    conn.close()
    return jsonify({
        'increases': [dict(ix) for ix in increases],
        'decreases': [dict(ix) for ix in decreases]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
