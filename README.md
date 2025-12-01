# Quick start

### Create a virtualenv and install dependencies:
```python
python3 -m venv venv
```
```python
source venv/bin/activate # or venv\Scripts\activate on Windows
```
```python
pip3 install -r requirements.txt
```

---

### Start the API server:

```python
python3 -m uvicorn api.main:app --reload --port 8080
```

---

### In another terminal, use the CLI:

```python
source venv/bin/activate # or venv\Scripts\activate on Windows
```

```python
python cli/vulncli.py add
```
```python
python cli/vulncli.py list
```
```python
python cli/vulncli.py get <ID>
```
```python
python cli/vulncli.py update <ID>
```
```python
python cli/vulncli.py delete <ID>
```
