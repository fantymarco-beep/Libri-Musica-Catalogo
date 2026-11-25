import os
import sys
import json
import datetime
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database_libri.json")

def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/api/libri', methods=['GET'])
def get_libri():
    data = load_db()
    return jsonify(data)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    data = load_db()
    total = len(data)
    uploaded = sum(1 for d in data if d.get('caricato_gemini', False))
    remaining = total - uploaded
    pct = round((uploaded / total * 100), 1) if total > 0 else 0
    
    # by category
    by_cat = {}
    for d in data:
        cat = d.get('categoria', 'Altro')
        if cat not in by_cat:
            by_cat[cat] = {"total": 0, "uploaded": 0}
        by_cat[cat]["total"] += 1
        if d.get('caricato_gemini', False):
            by_cat[cat]["uploaded"] += 1
            
    return jsonify({
        "total": total,
        "uploaded": uploaded,
        "remaining": remaining,
        "percentage": pct,
        "by_category": by_cat
    })

@app.route('/api/libri/toggle', methods=['POST'])
def toggle_uploaded():
    payload = request.get_json() or {}
    item_id = payload.get('id')
    if item_id is None:
        return jsonify({"error": "Missing id"}), 400
        
    data = load_db()
    target_item = None
    for item in data:
        if item['id'] == item_id:
            item['caricato_gemini'] = not item.get('caricato_gemini', False)
            if item['caricato_gemini']:
                item['data_caricamento'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            else:
                item['data_caricamento'] = ""
            target_item = item
            break
            
    if target_item:
        save_db(data)
        return jsonify({"success": True, "item": target_item})
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/libri/note', methods=['POST'])
def update_note():
    payload = request.get_json() or {}
    item_id = payload.get('id')
    note_text = payload.get('note', '')
    
    data = load_db()
    target_item = None
    for item in data:
        if item['id'] == item_id:
            item['note'] = note_text
            target_item = item
            break
            
    if target_item:
        save_db(data)
        return jsonify({"success": True, "item": target_item})
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/libri/open', methods=['POST'])
def open_file():
    payload = request.get_json() or {}
    item_id = payload.get('id')
    data = load_db()
    for item in data:
        if item['id'] == item_id:
            filepath = item.get('percorso_assoluto')
            if filepath and os.path.exists(filepath):
                try:
                    os.startfile(filepath)
                    return jsonify({"success": True, "path": filepath})
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            else:
                return jsonify({"error": "File non trovato su disco"}), 404
    return jsonify({"error": "Item non trovato"}), 404

if __name__ == '__main__':
    port = 5055
    print(f"=== Catalogo Libri Musica avviato su http://localhost:{port} ===")
    app.run(host='127.0.0.1', port=port, debug=False)
