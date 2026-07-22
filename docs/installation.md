# Guia de Instalação

Este guia apresenta os requisitos e o passo a passo necessário para configurar o ambiente e executar os scripts de coleta de dados de rede móvel em dispositivos Android.

---

## 📋 Pré-requisitos

### Hardware
* **Smartphone Android**
* **Cabo USB** (para conexão com o computador)

### Software
* **Python** 3.10 ou superior
* **Android SDK Platform Tools (ADB)**
* **Git** *(opcional, para clonar o repositório)*

---

## 🚀 Passo a Passo de Instalação

### 1. Obter o Projeto
Clone o repositório para a sua máquina local e acesse a pasta do projeto:

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

### 2. Instalar Dependências do Python
Instale as bibliotecas necessárias para o funcionamento dos *parsers*:

```bash
pip install -r requirements.txt
```

### 3. Instalar o Android Platform Tools (ADB)
1. Baixe o pacote oficial do [Android Platform Tools](https://developer.android.com/tools/releases/platform-tools).
2. Extraia os arquivos para a pasta de sua preferência.
3. *(Recomendado)* Adicione o caminho da pasta do ADB à variável de ambiente `PATH` do seu sistema operacional.

---

## 📱 Configuração do Dispositivo Android

### Habilitar a Depuração USB
No seu smartphone, siga os passos abaixo:

1. Acesse **Configurações → Sobre o telefone**.
2. Toque **7 vezes** sobre **Número da versão** (ou *Build number*) até ativar o modo de desenvolvedor.
3. Volte ao menu principal de configurações e acesse **Opções do desenvolvedor**.
4. Ative a opção **Depuração USB**.

---

## 🔍 Verificação da Conexão

Conecte o smartphone ao computador via cabo USB e execute as validações no terminal:

### 1. Validar Conexão do ADB
```bash
adb devices
```

> **Saída esperada:**
> ```text
> List of devices attached
> R58XXXXXXX    device
> ```

### 2. Validar Permissões de Shell
```bash
adb shell
```

> 💡 **Nota:** Se o terminal de comandos do Android abrir normalmente (ex: `shell@android:/ $`), a comunicação está funcionando corretamente. Digite `exit` para sair.

---

## 📁 Estrutura do Projeto

```text
Projeto/
│
├── scripts/       # Scripts para coleta de dados
├── parsers/       # Processadores dos dados coletados
├── experimentos/  # Configurações e logs de testes
├── docs/          # Documentação detalhada
├── requirements.txt
└── README.md
```

---

## 📖 Próximos Passos

Após finalizar a configuração, consulte as documentações específicas para prosseguir:

* `docs/scripts.md` — Descrição e uso dos scripts de coleta.
* `docs/parsers.md` — Guia de utilização dos *parsers*.
* `docs/experiments.md` — Configuração dos cenários experimentais.
