# api/main.py
from fastapi import FastAPI, HTTPException
from api.models import Vulnerability, Asset
from api.database import load_db, save_db

app = FastAPI(title="AegisLogger API", version="0.2")

# --- Vulnerability CRUD Operations ---

@app.get("/vulnerabilities")
def get_vulns():
    try:
        data = load_db()
        return data.get("vulnerabilities", []) 
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/vulnerabilities/{vuln_id}")
def get_vuln(vuln_id: int):
    try:
        data = load_db().get("vulnerabilities", [])
        for vuln in data:
            if vuln.get("id") == vuln_id:
                return vuln
        raise HTTPException(status_code=404, detail=f"Vulnerability with ID {vuln_id} not found")
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/vulnerabilities", status_code=201)
def create_vuln(vuln: Vulnerability):
    try:
        db_data = load_db()
        data = db_data.get("vulnerabilities", [])
        
        max_id = max(v.get("id", 0) for v in data) if data else 0
        new_id = max_id + 1
        
        vuln_dict = vuln.model_dump()
        vuln_dict["id"] = new_id
        
        data.append(vuln_dict)
        db_data["vulnerabilities"] = data
        save_db(db_data)
        
        return {"id": new_id, "status_code": 201}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/vulnerabilities/{vuln_id}")
def update_vuln(vuln_id: int, vuln: Vulnerability):
    try:
        db_data = load_db()
        data = db_data.get("vulnerabilities", [])
        
        try:
            index_to_update = next(i for i, v in enumerate(data) if v.get("id") == vuln_id)
        except StopIteration:
            raise HTTPException(status_code=404, detail=f"Vulnerability with ID {vuln_id} not found")
        
        update_data = vuln.model_dump(exclude_unset=True)
        data[index_to_update].update(update_data)
        data[index_to_update]["id"] = vuln_id
        
        db_data["vulnerabilities"] = data
        save_db(db_data)
        
        return {"updated_id": vuln_id, "status_code": 200}
        
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/vulnerabilities/{vuln_id}")
def delete_vuln(vuln_id: int):
    try:
        db_data = load_db()
        data = db_data.get("vulnerabilities", [])
        
        initial_length = len(data)
        new_data = [v for v in data if v.get("id") != vuln_id]

        if len(new_data) == initial_length:
            raise HTTPException(status_code=404, detail=f"Vulnerability with ID {vuln_id} not found")

        db_data["vulnerabilities"] = new_data
        save_db(db_data)
        
        return {"deleted_id": vuln_id, "status_code": 200}
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# --- Asset CRUD Operations ---

@app.get("/assets")
def get_assets():
    try:
        data = load_db()
        return data.get("assets", []) 
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):
    try:
        data = load_db().get("assets", [])
        for asset in data:
            if asset.get("id") == asset_id:
                return asset
        raise HTTPException(status_code=404, detail=f"Asset with ID {asset_id} not found")
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/assets", status_code=201)
def create_asset(asset: Asset):
    try:
        db_data = load_db()
        data = db_data.get("assets", [])
        
        max_id = max(a.get("id", 0) for a in data) if data else 0
        new_id = max_id + 1
        
        asset_dict = asset.model_dump()
        asset_dict["id"] = new_id
        
        data.append(asset_dict)
        db_data["assets"] = data
        save_db(db_data)
        
        return {"id": new_id, "status_code": 201}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, asset: Asset):
    try:
        db_data = load_db()
        data = db_data.get("assets", [])
        
        try:
            index_to_update = next(i for i, a in enumerate(data) if a.get("id") == asset_id)
        except StopIteration:
            raise HTTPException(status_code=404, detail=f"Asset with ID {asset_id} not found")
        
        update_data = asset.model_dump(exclude_unset=True)
        data[index_to_update].update(update_data)
        data[index_to_update]["id"] = asset_id
        
        db_data["assets"] = data
        save_db(db_data)
        
        return {"updated_id": asset_id, "status_code": 200}
        
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):
    try:
        db_data = load_db()
        data = db_data.get("assets", [])
        
        initial_length = len(data)
        new_data = [a for a in data if a.get("id") != asset_id]

        if len(new_data) == initial_length:
            raise HTTPException(status_code=404, detail=f"Asset with ID {asset_id} not found")

        db_data["assets"] = new_data
        save_db(db_data)
        
        return {"deleted_id": asset_id, "status_code": 200}
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    