import re
import sys
from pathlib import Path

import pandas as pd


if len(sys.argv) < 2:
    print("Uso:")
    print("python parse_logcat_ca.py <logcat.txt>")
    sys.exit(1)

LOG_FILE = Path(sys.argv[1])

if not LOG_FILE.exists():
    print(f"Arquivo não encontrado: {LOG_FILE}")
    sys.exit(1)

print(f"Processando {LOG_FILE}")

with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

dados = []

ultimo_servicestate = {}

ultimo_evento = None

i = 0

while i < len(linhas):

    linha = linhas[i]

    #
    # SERVICE STATE
    #
    if (
        "notifyServiceStateForSubId:" in linha
        or "ServiceState updated:" in linha
    ):

        bloco = linha

        voice_rat = re.search(
            r"getRilVoiceRadioTechnology=\d+\((.*?)\)",
            bloco
        )

        data_rat = re.search(
            r"getRilDataRadioTechnology=\d+\((.*?)\)",
            bloco
        )

        operator = re.search(
            r"mOperatorAlphaLong=([^,]+)",
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

        pci = re.search(
            r"mPci=(\d+)",
            bloco
        )

        earfcn = re.search(
            r"mEarfcn=(\d+)",
            bloco
        )

        band = re.search(
            r"mBands=\[(.*?)\]",
            bloco
        )

        ultimo_servicestate = {
            "operator":
                operator.group(1).strip()
                if operator else None,

            "voice_rat":
                voice_rat.group(1)
                if voice_rat else None,

            "data_rat":
                data_rat.group(1)
                if data_rat else None,

            "nr_available":
                nr_available.group(1)
                if nr_available else None,

            "endc_available":
                endc_available.group(1)
                if endc_available else None,

            "pci":
                pci.group(1)
                if pci else None,

            "earfcn":
                earfcn.group(1)
                if earfcn else None,

            "band":
                band.group(1)
                if band else None,
        }

    #
    # PHYSICAL CHANNEL CONFIG
    #
    elif "UNSOL_PHYSICAL_CHANNEL_CONFIG" in linha:

        timestamp = linha[:23]

        bloco = linha

        while (
            i + 1 < len(linhas)
            and "[PHONE" not in bloco
        ):
            i += 1
            bloco += linhas[i]

        canais = re.findall(
            r"mConnectionStatus=(PrimaryServing|SecondaryServing).*?"
            r"mDownlinkChannelNumber=(\d+).*?"
            r"mPhysicalCellId=(\d+).*?"
            r"mBand=(\d+)",
            bloco,
            re.DOTALL
        )

        if canais:

            pcell_band = None
            pcell_earfcn = None
            pci = None

            scells = []

            for status, earfcn, pci_tmp, band in canais:

                if status == "PrimaryServing":
                    pci = pci_tmp
                    pcell_band = band
                    pcell_earfcn = earfcn

                elif status == "SecondaryServing":
                    scells.append(
                        (band, earfcn)
                    )

            scell_band = None
            scell_earfcn = None

            if len(scells) > 0:
                scell_band = scells[0][0]
                scell_earfcn = scells[0][1]

            num_cells = len(canais)

            ca_active = num_cells > 1

            evento = (
                pci,
                pcell_band,
                pcell_earfcn,
                scell_band,
                scell_earfcn,
                num_cells,
                ultimo_servicestate.get("nr_available"),
                ultimo_servicestate.get("endc_available"),
            )

            if evento != ultimo_evento:

                dados.append({
                    "timestamp": timestamp,

                    "operator":
                        ultimo_servicestate.get("operator"),

                    "voice_rat":
                        ultimo_servicestate.get("voice_rat"),

                    "data_rat":
                        ultimo_servicestate.get("data_rat"),

                    "pci": pci,

                    "pcell_band": pcell_band,
                    "pcell_earfcn": pcell_earfcn,

                    "scell_band": scell_band,
                    "scell_earfcn": scell_earfcn,

                    "num_cells": num_cells,

                    "ca_active": ca_active,

                    "nr_available":
                        ultimo_servicestate.get("nr_available"),

                    "endc_available":
                        ultimo_servicestate.get("endc_available"),
                })

                ultimo_evento = evento

    i += 1

df = pd.DataFrame(dados)

arquivo_saida = (
    LOG_FILE.parent /
    f"{LOG_FILE.stem}_ca.csv"
)

df.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print()
print("===== RESUMO =====")
print(f"Eventos únicos: {len(df)}")
print(f"CSV salvo em: {arquivo_saida}"
