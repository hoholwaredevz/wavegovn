from flask import Flask, request, jsonify
import sqlite3
import uuid

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect('whitelist.db')
    return conn

@app.route('/set_hwid', methods=['POST'])
def set_hwid():
    data = request.json
    recovery_key = data.get('recovery_key')
    new_hwid = data.get('hwid')

    conn = connect_db()
    cursor = conn.cursor()

    # Находим аккаунт по recovery ключу
    cursor.execute("SELECT discord_id FROM accounts WHERE recovery_key = ?", (recovery_key,))
    account = cursor.fetchone()

    if account:
        discord_id = account[0]
        # Обновляем HWID
        cursor.execute(f"UPDATE account_{discord_id} SET hwid = ? WHERE recovery_key = ?", (new_hwid, recovery_key))
        conn.commit()
        return jsonify({"status": "success", "message": "HWID успешно обновлён."}), 200
    else:
        return jsonify({"status": "error", "message": "Аккаунт не найден."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
