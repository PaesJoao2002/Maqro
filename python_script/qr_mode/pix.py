import re

GUI_TEXT = "BR.GOV.BCB.PIX"

def crc16(payload: str) -> str:
    polinomy = 0x1021
    result = 0xFFFF

    for byte in payload.encode("utf-8"):
        result ^= byte << 8
        for _ in range(8):
            if result & 0x8000:
                result = (result << 1) ^ polinomy
            else:
                result <<= 1
            result &= 0xFFFF

    return f"{result:04X}"

def emv(id_: str, valor: str) -> str:
    tamanho = f"{len(valor):02}"
    return f"{id_}{tamanho}{valor}"

def normalizar_por_tipo(chave: str, tipo: str) -> str:
    chave = chave.strip()

    if tipo == "Telefone":
        numeros = re.sub(r"\D", "", chave)

        if len(numeros) not in (10, 11):
            raise ValueError("Telefone inválido")

        return "+55" + numeros

    elif tipo == "CPF":
        numeros = re.sub(r"\D", "", chave)

        if len(numeros) != 11:
            raise ValueError("CPF inválido")

        return numeros

    elif tipo == "CNPJ":
        numeros = re.sub(r"\D", "", chave)

        if len(numeros) != 14:
            raise ValueError("CNPJ inválido")

        return numeros

    elif tipo == "E-mail":
        return chave.lower()

    elif tipo == "Chave Aleatória":
        return chave

    else:
        raise ValueError("Tipo de chave desconhecido")

def gerar_payload_pix(chave: str, tipo: str, valor: float | None = None, txid: str = "***") -> str:
    chave = normalizar_por_tipo(chave, tipo)

    gui_field = emv("00", GUI_TEXT)
    chave_field = emv("01", chave)
    merchant_account = emv("26", gui_field + chave_field)

    payload = ""
    payload += emv("00", "01")
    payload += merchant_account
    payload += emv("52", "0000")
    payload += emv("53", "986")
    payload += emv("58", "BR")

    payload += emv("59", "N")
    payload += emv("60", "C")

    if valor is not None:
        valor_str = f"{valor:.2f}"
        payload += emv("54", valor_str)

    adicional = emv("05", txid)
    payload += emv("62", adicional)

    payload_crc = payload + "6304"
    crc = crc16(payload_crc)

    payload_final = payload_crc + crc

    return payload_final