# api/main.py
from fastapi import FastAPI, HTTPException
from api.models import Vulnerability
from api.database import load_db, save_db

app = FastAPI(title="AegisLogger API", version="0.1")

# get all vulns
@app.get("/vulnerabilities")
def get_vulns():
    try:
        data = load_db()
        return data
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# get one vuln by id
@app.get("/vulnerabilities/{vuln_id}")
def get_vuln(vuln_id: int):
    try:
        data = load_db()
        for vuln in data:
            if vuln.get("id") == vuln_id:
                return vuln
        raise HTTPException(status_code=404, detail=f"Vulnerability with ID {vuln_id} not found")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# create vuln by id
@app.post("/vulnerabilities", status_code=201)
def create_vuln(vuln: Vulnerability):
    try:
        data = load_db()
        max_id = max(v.get("id", 0) for v in data) if data else 0
        new_id = max_id + 1
        
        vuln_dict = vuln.model_dump()
        vuln_dict["id"] = new_id
        
        data.append(vuln_dict)
        save_db(data)
        
        return {"id": new_id, "status_code": 201}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# update vuln by id
@app.put("/vulnerabilities/{vuln_id}")
def update_vuln(vuln_id: int, vuln: Vulnerability):
    try:
        data = load_db()
        
        index_to_update = next(i for i, v in enumerate(data) if v.get("id") == vuln_id)

        update_data = vuln.model_dump(exclude_unset=True)
        data[index_to_update].update(update_data)
        data[index_to_update]["id"] = vuln_id
        save_db(data)
        
        return {"updated_id": vuln_id, "status_code": 200}
        
    except HTTPException:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# delete vuln by id
@app.delete("/vulnerabilities/{vuln_id}")
def delete_vuln(vuln_id: int):
    try:
        data = load_db()
        new_data = [v for v in data if v.get("id") != vuln_id]
        save_db(new_data)
        return {"deleted": vuln_id, "status_code": 200}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    