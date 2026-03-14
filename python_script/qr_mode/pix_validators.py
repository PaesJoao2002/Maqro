import re
from python_script.functional.error_messages import *


def validate_phone(raw: str) -> str:
    cleaned = re.sub(r"\D", "", raw)
    n = len(cleaned)

    if n != 11:
        raise ValueError(PIX_PHONE_INVALID)

    return cleaned


def validate_cpf(raw: str) -> str:
    cleaned = re.sub(r"\D", "", raw)
    n = len(cleaned)

    if n != 11:
        raise ValueError(PIX_CPF_INVALID)

    return cleaned


def validate_cnpj(raw: str) -> str:
    digits = re.sub(r"\D", "", raw)

    if len(digits) != 14:
        raise ValueError(PIX_CNPJ_INVALID)

    return digits


def validate_email(raw: str) -> str:
    email = raw.strip()
    pattern = r"^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$"

    if re.match(pattern, email) is None:
        raise ValueError(PIX_EMAIL_INVALID)

    return email


def validate_random_key(raw: str) -> str:
    key = raw.lower().replace("-", "")

    if len(key) != 32:
        raise ValueError(PIX_RANDOM_KEY_LENGTH_INVALID)

    # garante que só tem hex
    for ch in key:
        if ch not in "0123456789abcdef":
            raise ValueError(PIX_RANDOM_KEY_FORMAT_INVALID)

    return key