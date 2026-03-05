import re
from python_script.functional.error_messages import *

def validate_phone(raw: str) -> str:
    cleaned = re.sub(r"\D", "", raw)
    if len(cleaned) != 11:
        raise ValueError(PIX_PHONE_INVALID)
    return cleaned

def validate_cpf(raw: str) -> str:
    cleaned = re.sub(r"\D", "", raw)
    if len(cleaned) != 11:
        raise ValueError(PIX_CPF_INVALID)
    return cleaned

def validate_cnpj(raw: str) -> str:
    cleaned = re.sub(r"\D", "", raw)
    if len(cleaned) != 14:
        raise ValueError(PIX_CNPJ_INVALID)
    return cleaned

def validate_email(raw: str) -> str:
    pattern = r"^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, raw.strip()):
        raise ValueError(PIX_EMAIL_INVALID)
    return raw.strip()

def validate_random_key(raw: str) -> str:
    cleaned = raw.replace("-", "").lower()
    if len(cleaned) != 32:
        raise ValueError(PIX_RANDOM_KEY_LENGTH_INVALID)
    if not re.fullmatch(r"[0-9a-f]{32}", cleaned):
        raise ValueError(PIX_RANDOM_KEY_FORMAT_INVALID)
    return cleaned