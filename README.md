# Quick start

1. Create a virtualenv and install dependencies:
```
python3 -m venv venv
```
```
source venv/bin/activate # or venv\Scripts\activate on Windows
```
```
pip3 install -r requirements.txt
```

2. Start the API server:
```
python3 -m uvicorn api.main:app --reload
```

3. In another terminal, use the CLI:
```
source venv/bin/activate # or venv\Scripts\activate on Windows
```

```
python cli/vulncli.py add
```
```
python cli/vulncli.py list
```
```
python cli/vulncli.py get 1
```
```
python cli/vulncli.py update 1
```
```
python cli/vulncli.py delete 1
```
```
python cli/vulncli.py export
```
