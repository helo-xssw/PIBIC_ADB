# Installation Guide

Este guia apresenta os requisitos e os passos necessários para configurar o ambiente e executar os scripts de coleta de dados da rede móvel em dispositivos Android.

---

# Requirements

## Hardware

- Smartphone Android
- Cabo USB para conexão com o computador

## Software

- Python 3.10 ou superior
- Android SDK Platform Tools (ADB)
- Git (opcional, para clonar o repositório)

---

# Clone the repository

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git

cd SEU-REPOSITORIO
```

---

# Install Python dependencies

Instale as bibliotecas utilizadas pelos parsers.

```bash
pip install -r requirements.txt
```

---

# Install Android Platform Tools

Baixe o Android Platform Tools (ADB) no site oficial:

https://developer.android.com/tools/releases/platform-tools

Extraia os arquivos para uma pasta de sua preferência.

Opcionalmente, adicione a pasta do ADB à variável de ambiente PATH.

---

# Enable USB Debugging

No smartphone:

1. Abra **Settings → About phone**.
2. Toque sete vezes em **Build number** para habilitar as opções de desenvolvedor.
3. Acesse **Developer options**.
4. Ative **USB debugging**.

---

# Verify ADB connection

Conecte o smartphone ao computador e execute:

```bash
adb devices
```

A saída deverá ser semelhante a:

```text
List of devices attached

R58XXXXXXX    device
```

---

# Verify permissions

Execute:

```bash
adb shell
```

Se o terminal do Android abrir normalmente, a comunicação está funcionando.

---

# Project structure

```
Projeto/
│
├── scripts/
├── parsers/
├── experimentos/
├── docs/
├── requirements.txt
└── README.md
```

---

# Next steps

Após concluir a instalação, consulte:

- `docs/scripts.md` — descrição de cada script de coleta.
- `docs/parsers.md` — utilização dos parsers.
- `docs/experiments.md` — cenários experimentais.
