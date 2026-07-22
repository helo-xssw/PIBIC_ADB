import subprocess
import time
from datetime import datetime
from pathlib import Path

ADB_PATH = Path(r"C:\adb\platform-tools\adb.exe")

print("Selecione o cenário do experimento:")
print("1 - Laboratório")
print("2 - Cenário Real")

opcao = input("Escolha: ")

if opcao == "1":
    CENARIO = "laboratorio"
elif opcao == "2":
    CENARIO = "cenario_real"
else:
    print("[ERRO] Opção inválida.")
    exit()

try:
    INTERVALO = float(
        input("Intervalo entre coletas (segundos): ")
    )

    DURACAO = int(
        input("Duração total da coleta (segundos): ")
    )
except ValueError:
    print("[ERRO] Digite apenas números.")
    exit()

if INTERVALO < 0.1:
    print("\n[AVISO CRÍTICO]")
    print("Intervalos muito baixos podem:")
    print("- sobrecarregar o Android")
    print("- aquecer o modem")
    print("- distorcer métricas")
    print("-> Ajustando automaticamente para 0.1s.\n")

    INTERVALO = 0.1

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

PASTA = (
    Path("experiments")
    / CENARIO
    / "servicestate"
    / timestamp
)

PASTA.mkdir(parents=True, exist_ok=True)

RAW_LOG = PASTA / "raw.log"
META = PASTA / "metadata.txt"

with open(META, "w", encoding="utf-8") as f:
    f.write(f"Dispositivo: {DISPOSITIVO}\n")
    f.write(f"Android: {ANDROID}\n")
    f.write(f"Operadora: {OPERADORA}\n")
    f.write(f"Tecnologia: {TECNOLOGIA}\n")
    f.write(f"Cenário: {CENARIO}\n")
    f.write(f"Método: servicestate\n")
    f.write(f"Intervalo: {INTERVALO}s\n")
    f.write(f"Duração: {DURACAO}s\n")
    f.write(f"Data: {timestamp}\n")

print("\n[INFO] Iniciando coleta...")
print(f"[INFO] Dispositivo detectado: {DISPOSITIVO}")
print(f"[INFO] Android: {ANDROID}")
print(f"[INFO] Logs serão salvos em:\n{PASTA}\n")

KEYWORDS = [
    "servicestate",       
    "voiceregstate",     
    "dataregstate",       
    "operatoralpha",      
    "earfcn",            
    "bands",             
    "carrieraggregation", 
    "networkregistration",
    "displayinfo"        
]

inicio = time.time()

coletas_realizadas = 0
linhas_salvas = 0

with open(RAW_LOG, "w", encoding="utf-8", errors="ignore") as log:

    while time.time() - inicio < DURACAO:

        tempo_loop_start = time.time()

        momento = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3]

        try:
            resultado = subprocess.check_output(
                [
                    str(ADB_PATH),
                    "shell",
                    "dumpsys",
                    "telephony.registry"
                ],
                text=True,
                encoding="utf-8",
                errors="ignore",
                stderr=subprocess.STDOUT
            )

            linhas_filtradas = []

            for linha in resultado.splitlines():
                linha_limpa = linha.strip()
                linha_lower = linha_limpa.lower()

                # Se qualquer uma das palavras-chave simplificadas estiver na linha
                if any(kw in linha_lower for kw in KEYWORDS):
                    linhas_filtradas.append(linha_limpa)

            if linhas_filtradas:
                log.write(f"\n===== COLETA {momento} =====\n")
                
                for linha in linhas_filtradas:
                    log.write(linha + "\n")

                log.flush()

                coletas_realizadas += 1
                linhas_salvas += len(linhas_filtradas)

                print(
                    f"[OK] Coleta realizada: "
                    f"{momento.split()[1]} | "
                    f"Linhas: {len(linhas_filtradas)}"
                )
            else:
                print(
                    f"[AVISO] Nenhum dado relevante encontrado às "
                    f"{momento.split()[1]}"
                )

        except subprocess.CalledProcessError:
            print(
                f"[ALERTA CRÍTICO] "
                f"Falha na comunicação ADB às "
                f"{momento.split()[1]}"
            )

        except Exception as e:
            print(f"[ERRO] {e}")

        tempo_gasto = time.time() - tempo_loop_start

        if tempo_gasto > INTERVALO:
            print(
                f"[AVISO] Overhead detectado! "
                f"Execução demorou {tempo_gasto:.3f}s"
            )
            tempo_sono = 0.01
        else:
            tempo_sono = INTERVALO - tempo_gasto

        time.sleep(tempo_sono)

tamanho_mb = RAW_LOG.stat().st_size / (1024 * 1024)

print("\n[INFO] Coleta finalizada com sucesso.")
print(f"[INFO] Total de snapshots: {coletas_realizadas}")
print(f"[INFO] Total de linhas salvas: {linhas_salvas}")
print(f"[INFO] Tamanho final do log: {tamanho_mb:.2f} MB")
print(f"[INFO] Arquivo salvo em:\n{RAW_LOG}")
