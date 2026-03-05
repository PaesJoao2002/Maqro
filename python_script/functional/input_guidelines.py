import re

def clean_numeric(text: str) -> str:
    return re.sub(r"\D", "", text)


def clean_uuid(text: str) -> str:
    return text.replace("-", "").lower()

def format_phone(text: str) -> str:
    raw = clean_numeric(text)[:11]

    if len(raw) >= 7:
        return f"({raw[:2]}) {raw[2:7]}-{raw[7:]}"
    if len(raw) >= 2:
        return f"({raw[:2]}) {raw[2:]}"
    return raw


def format_cpf(text: str) -> str:
    raw = clean_numeric(text)[:11]

    if len(raw) >= 9:
        return f"{raw[:3]}.{raw[3:6]}.{raw[6:9]}-{raw[9:]}"
    if len(raw) >= 6:
        return f"{raw[:3]}.{raw[3:6]}.{raw[6:]}"
    if len(raw) >= 3:
        return f"{raw[:3]}.{raw[3:]}"
    return raw


def format_cnpj(text: str) -> str:
    raw = clean_numeric(text)[:14]

    if len(raw) >= 12:
        return f"{raw[:2]}.{raw[2:5]}.{raw[5:8]}/{raw[8:12]}-{raw[12:]}"
    if len(raw) >= 8:
        return f"{raw[:2]}.{raw[2:5]}.{raw[5:8]}/{raw[8:]}"
    if len(raw) >= 5:
        return f"{raw[:2]}.{raw[2:5]}.{raw[5:]}"
    if len(raw) >= 2:
        return f"{raw[:2]}.{raw[2:]}"
    return raw

def validate_pix(key_type: str, raw_text: str):

    if key_type == "Telefone":
        text = clean_numeric(raw_text)
        if len(text) != 11:
            return None, "phone_invalid"
        return text, None

    if key_type == "CPF":
        text = clean_numeric(raw_text)
        if len(text) != 11:
            return None, "cpf_invalid"
        return text, None

    if key_type == "CNPJ":
        text = clean_numeric(raw_text)
        if len(text) != 14:
            return None, "cnpj_invalid"
        return text, None

    if key_type == "E-mail":
        pattern = r"^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, raw_text):
            return None, "email_invalid"
        return raw_text, None

    if key_type == "Chave Aleatória":
        cleaned = clean_uuid(raw_text)

        if len(cleaned) != 32:
            return None, "uuid_length"

        if not re.fullmatch(r"[0-9a-f]{32}", cleaned):
            return None, "uuid_format"

        return cleaned, None

    return None, "unknown_type"