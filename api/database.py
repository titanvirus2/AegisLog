import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "vuln_db.txt" 
DATA_DIR.mkdir(parents=True, exist_ok=True)

INITIAL_DB_STATE = {
    "vulnerabilities": [],
    "assets": []
}

def load_db():
    if not DB_PATH.exists():
        content = json.dumps(INITIAL_DB_STATE, indent=2)
        DB_PATH.write_text(content, encoding="utf-8")
        return INITIAL_DB_STATE
        
    try:
        data = json.loads(DB_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
             raise json.JSONDecodeError("DB content is not a dictionary", DB_PATH.name, 0)
        for key in INITIAL_DB_STATE:
            if key not in data:
                data[key] = INITIAL_DB_STATE[key]
        return data
        
    except json.JSONDecodeError:
        content = json.dumps(INITIAL_DB_STATE, indent=2)
        DB_PATH.write_text(content, encoding="utf-8")
        return INITIAL_DB_STATE

def save_db(data: dict):
    content = json.dumps(data, indent=2)
    DB_PATH.write_text(content, encoding="utf-8")
    