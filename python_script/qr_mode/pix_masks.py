import re

def apply_phone_mask(text: str) -> str:
    raw = re.sub(r"\D", "", text)[:11]
    formatted = raw
    if len(raw) >= 2:
        formatted = f"({raw[:2]}) {raw[2:]}"
    if len(raw) >= 7:
        formatted = f"({raw[:2]}) {raw[2:7]}-{raw[7:]}"
    return formatted

def apply_cpf_mask(text: str) -> str:
    raw = re.sub(r"\D", "", text)[:11]
    formatted = raw
    if len(raw) >= 3:
        formatted = f"{raw[:3]}.{raw[3:]}"
    if len(raw) >= 6:
        formatted = f"{raw[:3]}.{raw[3:6]}.{raw[6:]}"
    if len(raw) >= 9:
        formatted = f"{raw[:3]}.{raw[3:6]}.{raw[6:9]}-{raw[9:]}"
    return formatted

def apply_cnpj_mask(text: str) -> str:
    raw = re.sub(r"\D", "", text)[:14]
    formatted = raw
    if len(raw) >= 2:
        formatted = f"{raw[:2]}.{raw[2:]}"
    if len(raw) >= 5:
        formatted = f"{raw[:2]}.{raw[2:5]}.{raw[5:]}"
    if len(raw) >= 8:
        formatted = f"{raw[:2]}.{raw[2:5]}.{raw[5:8]}/{raw[8:]}"
    if len(raw) >= 12:
        formatted = f"{raw[:2]}.{raw[2:5]}.{raw[5:8]}/{raw[8:12]}-{raw[12:]}"
    return formatted