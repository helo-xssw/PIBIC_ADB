import re
import sys
from pathlib import Path
import pandas as pd

if len(sys.argv) < 2:
    print("Uso:")
    print("python parse_signalstrength.py <caminho_para_raw.log>")
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
cell_rows = []

for i in range(1, len(blocos), 2):

    timestamp = blocos[i].strip()
    bloco = blocos[i + 1]



    lte_match = re.search(
        r"mLte=CellSignalStrengthLte:.*?"
        r"rsrp=(-?\d+).*?"
        r"rsrq=(-?\d+).*?"
        r"rssnr=(-?\d+).*?"
        r"cqi=(\d+)",
        bloco,
        re.DOTALL
    )

    nr_match = re.search(
        r"mNr=CellSignalStrengthNr:\{.*?"
        r"ssRsrp\s*=\s*(-?\d+).*?"
        r"ssRsrq\s*=\s*(-?\d+).*?"
        r"ssSinr\s*=\s*(-?\d+)",
        bloco,
        re.DOTALL
    )

    summary_rows.append({
        "timestamp": timestamp,
        "lte_rsrp": lte_match.group(1) if lte_match else None,
        "lte_rsrq": lte_match.group(2) if lte_match else None,
        "lte_rssnr": lte_match.group(3) if lte_match else None,
        "lte_cqi": lte_match.group(4) if lte_match else None,
        "nr_ssrsrp": nr_match.group(1) if nr_match else None,
        "nr_ssrsrq": nr_match.group(2) if nr_match else None,
        "nr_sssinr": nr_match.group(3) if nr_match else None,
    })

   

    lte_lista = list(re.finditer(
        r"CellInfoLte:\{"
        r".*?mRegistered=(YES|NO)"
        r".*?mPci=(\d+)"
        r".*?mEarfcn=(\d+)"
        r".*?mBands=\[(\d+)\]"
        r".*?rsrp=(-?\d+)"
        r".*?rsrq=(-?\d+)"
        r".*?rssnr=(-?\d+)",
        bloco,
        re.DOTALL
    ))

    

    nr_lista = list(re.finditer(
        r"CellInfoNr:\{"
        r".*?mRegistered=(YES|NO)"
        r".*?mPci\s*=\s*(\d+)"
        r".*?mNrArfcn\s*=\s*(\d+)"
        r".*?mBands\s*=\s*\[(\d+)\]"
        r".*?ssRsrp\s*=\s*(-?\d+)"
        r".*?ssRsrq\s*=\s*(-?\d+)"
        r".*?ssSinr\s*=\s*(-?\d+)",
        bloco,
        re.DOTALL
    ))

    total_cells = len(lte_lista) + len(nr_lista)

    if total_cells > 20:
        print(
            f"[SUSPEITO] {timestamp} -> "
            f"LTE={len(lte_lista)} NR={len(nr_lista)} "
            f"TOTAL={total_cells}"
        )

    for m in lte_lista:

        cell_rows.append({
            "timestamp": timestamp,
            "tecnologia": "LTE",
            "registered": m.group(1),
            "pci": m.group(2),
            "banda": m.group(4),
            "arfcn": m.group(3),
            "rsrp": m.group(5),
            "rsrq": m.group(6),
            "sinr": m.group(7)
        })

    for m in nr_lista:

        cell_rows.append({
            "timestamp": timestamp,
            "tecnologia": "NR",
            "registered": m.group(1),
            "pci": m.group(2),
            "banda": m.group(4),
            "arfcn": m.group(3),
            "rsrp": m.group(5),
            "rsrq": m.group(6),
            "sinr": m.group(7)
        })



pasta_saida = LOG_FILE.parent

arquivo_summary = pasta_saida / "signalstrength_summary.csv"
arquivo_cells = pasta_saida / "signalstrength_cells.csv"

if summary_rows:

    df_summary = pd.DataFrame(summary_rows)

    df_summary.to_csv(
        arquivo_summary,
        index=False,
        encoding="utf-8-sig"
    )

if cell_rows:

    df_cells = pd.DataFrame(cell_rows)

    df_cells.to_csv(
        arquivo_cells,
        index=False,
        encoding="utf-8-sig"
    )



print()
print("===== RESUMO =====")
print(f"Registros summary: {len(summary_rows)}")
print(f"Registros cells: {len(cell_rows)}")
print()
print(f"CSV Summary: {arquivo_summary}")
print(f"CSV Cells:   {arquivo_cells}")
