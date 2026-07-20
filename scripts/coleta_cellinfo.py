import subprocess
import time
from datetime import datetime
from pathlib import Path


ADB_PATH = Path(r"C:\adb\platform-tools\adb.exe")

print("Selecione o cenário do experimento:")
print("1 - Laboratório")
print("2 - Cenário Real (Laborátorio - Indoor)")

opcao = input("Escolha: ")

if opcao == "1":
    CENARIO = "laboratorio"
elif opcao == "2":
    CENARIO = "cenario_real"
else:
    print("[ERRO] Opção inválida.")
    exit()

try:
    INTERVALO = float(input("Intervalo entre coletas (segundos): "))
    DURACAO = int(input("Duração total da coleta (segundos): "))
except ValueError:
    print("[ERRO] Digite apenas números válidos.")
    exit()

def get_prop(prop):
    try:
        comando = [str(ADB_PATH), "shell", "getprop", prop]
        resultado = subprocess.check_output(comando, text=True, encoding="utf-8", errors="ignore").strip()
        return resultado if resultado else "Desconhecido"
    except Exception:
        return "Desconhecido"

dispositivo = get_prop("ro.product.model")
android = get_prop("ro.build.version.release")
operadora = input("Operadora: ")
tecnologia = input("Tecnologia utilizada (LTE/5G/etc): ")

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
PASTA = Path(f"experiments/{CENARIO}/cellinfo/{timestamp}")
PASTA.mkdir(parents=True, exist_ok=True)

RAW_LOG = PASTA / "raw.log"
META = PASTA / "metadata.txt"

with open(META, "w", encoding="utf-8") as f:
    f.write(f"Dispositivo: {dispositivo}\nAndroid: {android}\nOperadora: {operadora}\n")
    f.write(f"Tecnologia: {tecnologia}\nCenário: {CENARIO}\nIntervalo: {INTERVALO}s\n")
    f.write(f"Duração: {DURACAO}s\nData: {timestamp}\n")

print("\n[INFO] Iniciando coleta estrita...")
inicio = time.time()

with open(RAW_LOG, "a", encoding="utf-8", errors="ignore") as log:

    while time.time() - inicio < DURACAO:
        tempo_ciclo_inicio = time.time()
        timestamp_coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        try:
            comando = [str(ADB_PATH), "shell", "dumpsys", "telephony.registry"]
            resultado = subprocess.check_output(comando, text=True, encoding="utf-8", errors="ignore", stderr=subprocess.STDOUT)

            linhas = resultado.splitlines()
            bloco_valido = None

            for linha in linhas:
                linha_focada = linha.strip()
                
                # Procura a linha que inicia com mCellInfo e garante que ela contém dados reais (contém "CellInfo")
                if linha_focada.startswith("mCellInfo=[") and "CellInfo" in linha_focada:
                    bloco_valido = linha_focada
                    break # Encontrou o dado real da rodada, pode parar a busca no dump atual

            if bloco_valido:
                log.write(f"\n===== COLETA {timestamp_coleta} =====\n")
                log.write(bloco_valido + "\n")
                log.flush()
                print(f"[OK] Coleta realizada: {timestamp_coleta.split()[1]} | Dados de rádio salvos.")
            else:
                print(f"[AVISO] Nenhum dado de rádio válido às {timestamp_coleta.split()[1]}.")

        except subprocess.CalledProcessError:
            print(f"[ALERTA CRÍTICO] Falha de hardware/cabo às {timestamp_coleta.split()[1]}.")
        except Exception as e:
            print(f"[ERRO] {e}")

        tempo_passado = time.time() - tempo_ciclo_inicio
        time.sleep(max(0.01, INTERVALO - tempo_passado))

print("\n[INFO] Coleta encerrada com sucesso. Log limpo gerado.")
