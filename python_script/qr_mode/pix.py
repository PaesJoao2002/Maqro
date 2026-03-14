import re

GUI_TEXT = "BR.GOV.BCB.PIX"


def crc16(payload: str) -> str:
    poly = 0x1021
    crc = 0xFFFF

    data = payload.encode("utf-8")

    for b in data:
        crc ^= b << 8

        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1

            crc &= 0xFFFF

    return f"{crc:04X}"


def emv(tag: str, value: str) -> str:
    size = f"{len(value):02}"
    return f"{tag}{size}{value}"


# -------------------------
# Normalização das chaves
# -------------------------

def _norm_telefone(chave: str) -> str:
    nums = re.sub(r"\D", "", chave)

    if not 10 <= len(nums) <= 11:
        raise ValueError("Telefone inválido")

    return "+55" + nums


def _norm_cpf(chave: str) -> str:
    nums = re.sub(r"\D", "", chave)

    if len(nums) != 11:
        raise ValueError("CPF inválido")

    return nums


def _norm_cnpj(chave: str) -> str:
    nums = re.sub(r"\D", "", chave)

    if len(nums) != 14:
        raise ValueError("CNPJ inválido")

    return nums


def _norm_email(chave: str) -> str:
    return chave.strip().lower()


def _norm_random(chave: str) -> str:
    return chave.strip()


_NORMALIZERS = {
    "Telefone": _norm_telefone,
    "CPF": _norm_cpf,
    "CNPJ": _norm_cnpj,
    "E-mail": _norm_email,
    "Chave Aleatória": _norm_random,
}


def normalizar_por_tipo(chave: str, tipo: str) -> str:
    chave = chave.strip()

    fn = _NORMALIZERS.get(tipo)
    if fn is None:
        raise ValueError(f"Tipo de chave desconhecido: {tipo}")

    return fn(chave)


# -------------------------
# Geração do payload PIX
# -------------------------

def gerar_payload_pix(
    chave: str,
    tipo: str,
    valor: float | None = None,
    txid: str = "***"
) -> str:

    chave = normalizar_por_tipo(chave, tipo)

    gui = emv("00", GUI_TEXT)
    chave_pix = emv("01", chave)
    merchant_account = emv("26", gui + chave_pix)

    payload = ""

    # payload format indicator
    payload += emv("00", "01")

    # merchant account info
    payload += merchant_account

    # campos fixos
    payload += (
        emv("52", "0000") +
        emv("53", "986") +
        emv("58", "BR")
    )

    # nome e cidade (mínimo obrigatório)
    payload += emv("59", "N")
    payload += emv("60", "C")

    if valor is not None:
        payload += emv("54", f"{valor:.2f}")

    adicional = emv("05", txid)
    payload += emv("62", adicional)

    # CRC final
    base = payload + "6304"
    checksum = crc16(base)

    return base + checksum