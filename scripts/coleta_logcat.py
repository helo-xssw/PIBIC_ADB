import subprocess
import time
from pathlib import Path
from datetime import datetime

ADB_PATH = Path(r"C:\adb\platform-tools\adb.exe")

print("Selecione o cenário do experimento:")
print("1 - Laboratório")
print("2 - Cenário Real (Hall da Faculdade)")

opcao = input("Escolha: ")

if opcao == "1":
    CENARIO = "laboratorio"
elif opcao == "2":
    CENARIO = "cenario_real"
else:
    print("[ERRO] Opção inválida.")
    exit()

try:
    DURACAO = int(input("Duração total da coleta (segundos): "))
except ValueError:
    print("[ERRO] Digite apenas números.")
    exit()

def get_prop(prop):
    try:
        comando = [
            str(ADB_PATH),
            "shell",
            "getprop",
            prop
        ]

        resultado = subprocess.check_output(
            comando,
            text=True,
            encoding="utf-8",
            errors="ignore"
        ).strip()

        return resultado if resultado else "Desconhecido"

    except Exception:
        return "Desconhecido"

DISPOSITIVO = get_prop("ro.product.model")
ANDROID = get_prop("ro.build.version.release")


OPERADORA = input("Operadora: ")
TECNOLOGIA = input("Tecnologia utilizada (LTE/5G/etc): ")


timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

BASE_DIR = Path("experiments") / CENARIO / "logcat_radio" / timestamp
BASE_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = BASE_DIR / "raw.log"
METADATA_FILE = BASE_DIR / "metadata.txt"

with open(METADATA_FILE, "w", encoding="utf-8") as f:
    f.write(f"Dispositivo: {DISPOSITIVO}\n")
    f.write(f"Android: {ANDROID}\n")
    f.write(f"Operadora: {OPERADORA}\n")
    f.write(f"Tecnologia: {TECNOLOGIA}\n")
    f.write(f"Cenário: {CENARIO}\n")
    f.write(f"Método: logcat_radio\n")
    f.write(f"Duração: {DURACAO}s\n")
    f.write(f"Data: {timestamp}\n")

TERMOS_FILTRO = [
    "onCellInfoChanged",
    "onSignalStrengthsChanged",
    "onServiceStateChanged",
    "NetworkRegistrationInfo",
    "RILJ"
]

print("\n[INFO] Limpando logcat antigo...")

subprocess.run(
    [str(ADB_PATH), "logcat", "-b", "radio", "-c"],
    capture_output=True
)

print("\n[INFO] Iniciando coleta logcat radio...")
print(f"[INFO] Dispositivo detectado: {DISPOSITIVO}")
print(f"[INFO] Android: {ANDROID}")
print(f"[INFO] Logs serão salvos em:\n{BASE_DIR}\n")

inicio = time.time()
linhas_salvas = 0

processo = subprocess.Popen(
    [
        str(ADB_PATH),
        "logcat",
        "-b",
        "radio",
        "-v",
        "year"
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True,
    encoding="utf-8",
    errors="ignore"
)

with open(LOG_FILE, "w", encoding="utf-8", errors="ignore") as log:

    try:
        while time.time() - inicio < DURACAO:

            linha = processo.stdout.readline()

            if not linha:
                continue

            linha_limpa = linha.strip()

            if any(termo in linha_limpa for termo in TERMOS_FILTRO):

                log.write(linha_limpa + "\n")
                log.flush()

                linhas_salvas += 1

                # Exibe status a cada 50 linhas
                if linhas_salvas % 50 == 0:
                    print(f"[INFO] {linhas_salvas} eventos relevantes salvos...")

    except KeyboardInterrupt:
        print("\n[INFO] Coleta interrompida manualmente.")

    except Exception as e:
        print(f"[ERRO] {e}")

    finally:
        print("\n[INFO] Finalizando processo do ADB...")

        processo.kill()
        processo.wait()

print(f"[INFO] Coleta finalizada com sucesso.")
print(f"[INFO] Total de eventos salvos: {linhas_salvas}")
print(f"[INFO] Arquivo salvo em:\n{LOG_FILE}")
