import re
import sys
from pathlib import Path
import pandas as pd

if len(sys.argv) < 2:
    print("Uso:")
    print("python parse_servicestate.py <caminho_para_raw.log>")
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

dados = []

for i in range(1, len(blocos), 2):

    timestamp = blocos[i].strip()
    bloco = blocos[i + 1]

    voice_reg = re.search(
        r"mVoiceRegState=\d+\((.*?)\)",
        bloco
    )

    data_reg = re.search(
        r"mDataRegState=\d+\((.*?)\)",
        bloco
    )

    operator = re.search(
        r"mOperatorAlphaLong=([^,]+)",
        bloco
    )

    channel = re.search(
        r"mChannelNumber=(-?\d+)",
        bloco
    )

    voice_rat = re.search(
        r"getRilVoiceRadioTechnology=\d+\((.*?)\)",
        bloco
    )

    data_rat = re.search(
        r"getRilDataRadioTechnology=\d+\((.*?)\)",
        bloco
    )

    nr_available = re.search(
        r"isNrAvailable\s*=\s*(true|false)",
        bloco
    )

    endc_available = re.search(
        r"isEnDcAvailable\s*=\s*(true|false)",
        bloco
    )

    display = re.search(
        r"overrideNetwork=([A-Z_]+)",
        bloco
    )

    cell = re.search(
        r"mCellIdentity=CellIdentityLte:\{.*?"
        r"mPci=(\d+).*?"
        r"mEarfcn=(\d+).*?"
        r"mBands=\[(.*?)\]",
        bloco,
        re.DOTALL
    )

    registro = {
        "timestamp": timestamp,

        "voice_reg_state":
            voice_reg.group(1) if voice_reg else None,

        "data_reg_state":
            data_reg.group(1) if data_reg else None,

        "operator":
            operator.group(1).strip() if operator else None,

        "channel_number":
            channel.group(1) if channel else None,

        "voice_rat":
            voice_rat.group(1) if voice_rat else None,

        "data_rat":
            data_rat.group(1) if data_rat else None,

        "nr_available":
            nr_available.group(1) if nr_available else None,

        "endc_available":
            endc_available.group(1) if endc_available else None,

        "override_network":
            display.group(1) if display else None,

        "pci":
            cell.group(1) if cell else None,

        "earfcn":
            cell.group(2) if cell else None,

        "band":
            cell.group(3) if cell else None,
    }

    dados.append(registro)

df = pd.DataFrame(dados)

arquivo_saida = LOG_FILE.parent / "servicestate.csv"

df.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print()
print("===== RESUMO =====")
print(f"Registros: {len(df)}")
print(f"CSV salvo em: {arquivo_saida}")
