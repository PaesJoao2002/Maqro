from python_script.functional.error_messages import *
import re

def validate_text(text: str) -> str:
    if not text.strip():
        raise ValueError(EMPTY_TEXT)
    return text.strip()

def validate_email(text: str) -> str:
    if not text.strip():
        raise ValueError(EMPTY_TEXT)
    pattern = r"^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$"
    if not re.fullmatch(pattern, text.strip()):
        raise ValueError(PIX_EMAIL_INVALID)
    return text.strip()

def validate_phone(text: str) -> str:
    raw = re.sub(r"\D", "", text)
    if len(raw) != 11:
        raise ValueError(PIX_PHONE_INVALID)
    return raw

def validate_cpf(text: str) -> str:
    raw = re.sub(r"\D", "", text)
    if len(raw) != 11:
        raise ValueError(PIX_CPF_INVALID)
    return raw

def validate_cnpj(text: str) -> str:
    raw = re.sub(r"\D", "", text)
    if len(raw) != 14:
        raise ValueError(PIX_CNPJ_INVALID)
    return raw

def validate_random_key(text: str) -> str:
    raw = text.replace("-", "").lower()
    if len(raw) != 32:
        raise ValueError(PIX_RANDOM_KEY_LENGTH_INVALID)
    elif not all(c in "0123456789abcdef" for c in raw):
        raise ValueError(PIX_RANDOM_KEY_FORMAT_INVALID)
    return raw