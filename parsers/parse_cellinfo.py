import re
import sys
from pathlib import Path
import pandas as pd


def extrair_registros(conteudo):

    registros = []

    blocos = re.split(
        r"===== COLETA ([\d\-]+\s[\d:\.]+) =====",
        conteudo
    )

    for i in range(1, len(blocos), 2):

        timestamp = blocos[i]
        bloco = blocos[i + 1]

        match = re.search(
            r"mRegistered=YES.*?"
            r"mPci=(\d+).*?"
            r"mEarfcn=(\d+).*?"
            r"mBands=\[(.*?)\].*?"
            r"mMcc=(\d+).*?"
            r"mMnc=(\d+).*?"
            r"mAlphaLong=([^\s]+).*?"
            r"rssi=(-?\d+).*?"
            r"rsrp=(-?\d+).*?"
            r"rsrq=(-?\d+).*?"
            r"rssnr=(-?\d+).*?"
            r"cqi=(\d+).*?"
            r"ta=(\d+).*?"
            r"level=(\d+)",
            bloco,
            re.DOTALL
        )

        if match:

            registros.append({
                "timestamp_coleta": timestamp,
                "pci": int(match.group(1)),
                "earfcn": int(match.group(2)),
                "banda": match.group(3),
                "mcc": int(match.group(4)),
                "mnc": int(match.group(5)),
                "operadora": match.group(6),
                "rssi": int(match.group(7)),
                "rsrp": int(match.group(8)),
                "rsrq": int(match.group(9)),
                "rssnr": int(match.group(10)),
                "cqi": int(match.group(11)),
                "ta": int(match.group(12)),
                "level": int(match.group(13))
            })

    return registros


if len(sys.argv) < 2:
    print("Uso:")
    print("python cell_info.py <caminho_para_raw.log>")
    sys.exit(1)

raw_log = Path(sys.argv[1])

if not raw_log.exists():
    print(f"Arquivo não encontrado: {raw_log}")
    sys.exit(1)

print("\n===== CELLINFO PARSER =====")
print(f"Arquivo: {raw_log}")

with open(raw_log, "r", encoding="utf-8", errors="ignore") as f:
    conteudo = f.read()

registros = extrair_registros(conteudo)

print(f"Registros encontrados: {len(registros)}")

if len(registros) == 0:
    print("Nenhum registro válido encontrado.")
    sys.exit(0)

df = pd.DataFrame(registros)

arquivo_saida = raw_log.parent / "cellinfo_parsed.csv"

df.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print(f"CSV criado: {arquivo_saida}")
print(f"Linhas exportadas: {len(df)}")
