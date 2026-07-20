import re
import sys
from pathlib import Path
import pandas as pd

if len(sys.argv) < 2:
    print("Uso:")
    print("python parse_min_telephony.py <caminho_para_raw.log>")
    sys.exit(1)

LOG_FILE = Path(sys.argv[1])

if not LOG_FILE.exists():
    print(f"Arquivo não encontrado: {LOG_FILE}")
    sys.exit(1)

print(f"Processando {LOG_FILE}")

with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
    texto = f.read()


blocos = re.split(
    r"===== COLETA ([0-9:\-\. ]+) =====",
    texto
)

summary_rows = []


for i in range(1, len(blocos), 2):

    timestamp = blocos[i].strip()
    bloco = blocos[i + 1]

    lte = re.search(
        r"mLte=CellSignalStrengthLte:.*?"
        r"rsrp=(-?\d+).*?"
        r"rsrq=(-?\d+).*?"
        r"rssnr=(-?\d+).*?"
        r"cqi=(\d+)",
        bloco,
        re.DOTALL
    )

    lte_cell = re.search(
        r"CellIdentityLte:\{.*?"
        r"mPci=(\d+).*?"
        r"mEarfcn=(\d+).*?"
        r"mBands=\[([^\]]+)\]",
        bloco,
        re.DOTALL
    )

    nr = re.search(
        r"CellSignalStrengthNr:\{.*?"
        r"ssRsrp\s*=\s*(-?\d+).*?"
        r"ssRsrq\s*=\s*(-?\d+).*?"
        r"ssSinr\s*=\s*(-?\d+)",
        bloco,
        re.DOTALL
    )

    has_nr = "CellSignalStrengthNr" in bloco
    has_lte = "CellSignalStrengthLte" in bloco

    if has_lte and has_nr:
        mode = "LTE+NR_NSA"
    elif has_lte:
        mode = "LTE"
    else:
        mode = "UNKNOWN"

    ca = "isUsingCarrierAggregation=true" in bloco
    en_dc = "isEnDcAvailable = true" in bloco

    sim1_ok = "Phone Id=0" in bloco and "IN_SERVICE" in bloco.split("Phone Id=0")[1].split("Phone Id=1")[0]

    summary_rows.append({
        "timestamp": timestamp,

        # MODE
        "mode": mode,
        "sim1_in_service": sim1_ok,

        # LTE RADIO
        "lte_rsrp": lte.group(1) if lte else None,
        "lte_rsrq": lte.group(2) if lte else None,
        "lte_sinr": lte.group(3) if lte else None,
        "lte_cqi": lte.group(4) if lte else None,

        # LTE CELL
        "lte_pci": lte_cell.group(1) if lte_cell else None,
        "lte_earfcn": lte_cell.group(2) if lte_cell else None,
        "lte_band": lte_cell.group(3) if lte_cell else None,

        # NR RADIO (5G)
        "nr_ssrsrp": nr.group(1) if nr else None,
        "nr_ssrsrq": nr.group(2) if nr else None,
        "nr_sssinr": nr.group(3) if nr else None,

        # FEATURES
        "carrier_aggregation": ca,
        "endc_5g_nsa": en_dc
    })

pasta_saida = LOG_FILE.parent
arquivo_summary = pasta_saida / "telephony_min_summary.csv"

df = pd.DataFrame(summary_rows)

df.to_csv(
    arquivo_summary,
    index=False,
    encoding="utf-8-sig"
)

print("\n===== RESUMO =====")
print(f"Registros: {len(summary_rows)}")
print(f"CSV: {arquivo_summary}")
