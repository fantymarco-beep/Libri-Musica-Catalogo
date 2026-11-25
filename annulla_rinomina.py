import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
log_file = os.path.join(os.path.dirname(__file__), 'rename_log.json')
if not os.path.exists(log_file):
    print("File rename_log.json non trovato!")
    sys.exit(1)

with open(log_file, 'r', encoding='utf-8') as f:
    records = json.load(f)

restored = 0
for r in records:
    if r.get('status') == 'renamed':
        cur = r['new_path']
        orig = r['old_path']
        if os.path.exists(cur):
            os.rename(cur, orig)
            restored += 1
print(f"Ripristinati {restored} file con successo.")
