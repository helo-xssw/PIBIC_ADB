import subprocess
import time
from datetime import datetime
import os
import argparse

# Caminho do ADB
ADB_PATH = r"C:\adb\platform-tools\adb.exe"

# -------------------------
# Argumentos via terminal
# -------------------------
parser = argparse.ArgumentParser(description="Coleta de logs via ADB")

parser.add_argument("--duracao", type=int, default=60, help="Duração da coleta em segundos")
parser.add_argument("--buffer", type=str, default="radio", help="Buffer do logcat (radio, main, system)")
parser.add_argument("--cenario", type=str, default="laboratorio", help="Cenário da coleta")

args = parser.parse_args()

# -------------------------
# Preparação de diretórios
# -------------------------
data_atual = datetime.now().strftime("%Y-%m-%d")
timestamp = datetime.now().strftime("%H-%M-%S")

base_path = f"logs/{args.cenario}/{data_atual}"
os.makedirs(base_path, exist_ok=True)

log_file = f"{base_path}/log_{args.buffer}_{timestamp}.txt"

# -------------------------
# Verificar conexão ADB
# -------------------------
print("Verificando dispositivos conectados...")
resultado = subprocess.run([ADB_PATH, "devices"], capture_output=True, text=True)

if "device" not in resultado.stdout:
    print("Nenhum dispositivo autorizado encontrado.")
    exit()

# -------------------------
# Limpar logs antigos
# -------------------------
print("Limpando logs antigos...")
subprocess.run([ADB_PATH, "logcat", "-c"])

# -------------------------
# Iniciar coleta
# -------------------------
print(f"Iniciando coleta: {args.buffer} por {args.duracao}s")

with open(log_file, "w", encoding="utf-8") as f:
    process = subprocess.Popen(
        [ADB_PATH, "logcat", "-b", args.buffer],
        stdout=f,
        stderr=subprocess.STDOUT,
        text=True
    )

    time.sleep(args.duracao)
    process.terminate()

print(f"Coleta finalizada: {log_file}")
