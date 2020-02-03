from pathlib import Path
import requests

token_path = Path(__file__).parents[1] / 'local' / 'token.txt'
with token_path.open('r') as f:
    token = f.read().strip()

