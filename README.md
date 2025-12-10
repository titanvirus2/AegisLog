# Quick start

### Create a virtualenv and install dependencies:
```python
python3 -m venv venv
```
```python
source venv/bin/activate # or venv\Scripts\activate on Windows
```
```python
pip3 install -r requirements.txt # or pip install -r requirements.txt on Windows
```

---

### Start the API server:

```python
python3 -m uvicorn api.main:app --reload --port 8080 # or python -m uvicorn api.main:app --reload --port 8080 on Windows
```

---

### In another terminal, use the CLI:

```python
source venv/bin/activate # or venv\Scripts\activate on Windows
```

```python
python3 cli/cli.py  # or python cli/cli.py on Windows
```
