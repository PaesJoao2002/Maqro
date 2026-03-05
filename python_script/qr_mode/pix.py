# pix.py
# Gerador de payload Pix padrão EMV (estático)
# Compatível com leitura por qualquer banco

import re

GUI = "BR.GOV.BCB.PIX"


# ---------------------------------------------------------
# CRC16-CCITT (0x1021) — obrigatório no Pix
# ---------------------------------------------------------
def _crc16(payload: str) -> str:
    polinomio = 0x1021
    resultado = 0xFFFF

    for byte in payload.encode("utf-8"):
        resultado ^= byte << 8
        for _ in range(8):
            if resultado & 0x8000:
                resultado = (resultado << 1) ^ polinomio
            else:
                resultado <<= 1
            resultado &= 0xFFFF

    return f"{resultado:04X}"


# ---------------------------------------------------------
# Formata campo EMV: ID + tamanho + valor
# ---------------------------------------------------------
def _emv(id_: str, valor: str) -> str:
    tamanho = f"{len(valor):02}"
    return f"{id_}{tamanho}{valor}"


# ---------------------------------------------------------
# Normaliza chave Pix automaticamente
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# Gera payload Pix
# chave  : chave pix (cpf, email, telefone, aleatória)
# valor  : opcional (None = QR aberto)
# txid   : identificador (*** recomendado para estático)
# ---------------------------------------------------------
def gerar_payload_pix(chave: str, tipo: str, valor: float | None = None, txid: str = "***") -> str:
    chave = normalizar_por_tipo(chave, tipo)

    # -------------------------------
    # Merchant Account Information (ID 26)
    # -------------------------------
    gui_field = _emv("00", GUI)
    chave_field = _emv("01", chave)
    merchant_account = _emv("26", gui_field + chave_field)

    # -------------------------------
    # Payload base EMV
    # -------------------------------
    payload = ""
    payload += _emv("00", "01")          # Payload Format Indicator
    payload += merchant_account
    payload += _emv("52", "0000")        # MCC fixo Pix
    payload += _emv("53", "986")         # Moeda BRL
    payload += _emv("58", "BR")          # País

    # Nome e cidade mínimos (evita rejeição)
    payload += _emv("59", "N")
    payload += _emv("60", "C")

    # -------------------------------
    # Valor (opcional)
    # -------------------------------
    if valor is not None:
        valor_str = f"{valor:.2f}"
        payload += _emv("54", valor_str)

    # -------------------------------
    # TXID (ID 62)
    # -------------------------------
    adicional = _emv("05", txid)
    payload += _emv("62", adicional)

    # -------------------------------
    # CRC (sempre último!)
    # -------------------------------
    payload_crc = payload + "6304"
    crc = _crc16(payload_crc)

    payload_final = payload_crc + crc

    return payload_final