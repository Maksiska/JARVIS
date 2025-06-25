import re

def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text.strip())

def contains_exit_command(text: str, exit_commands: list) -> bool:
    lowered = text.lower()
    return any(cmd in lowered for cmd in exit_commands)

def extract_keywords(text: str, keywords: list) -> list:
    return [kw for kw in keywords if kw in text.lower()]

def debug_log(msg: str):
    print(f"[DEBUG] {msg}")

def normalize_text_for_vector(text: str) -> str:
    text = clean_text(text)
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text
