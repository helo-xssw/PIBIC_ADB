# Guia de Instalação

Este guia apresenta os requisitos e o passo a passo necessário para configurar o ambiente e executar os scripts de coleta de dados de rede móvel em dispositivos Android.

---

##  Pré-requisitos

### Hardware
* **Smartphone Android**
* **Cabo USB** (para conexão com o computador)

### Software
* **Python** 3.10 ou superior
* **Android SDK Platform Tools (ADB)**
* **Git** *(opcional, para clonar o repositório)*

---

##  Passo a Passo de Instalação

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
2. Extraia os arquivos para um diretório no seu computador (exemplo: `C:\adb\platform-tools`).
3. *(Opcional)* Adicione o caminho da pasta do ADB às Variáveis de Ambiente do sistema para poder executar o comando de qualquer diretório.

---

##  Configuração do Dispositivo Android

> 💡 **Dica de Navegação:**
> O caminho para ativar o modo de desenvolvedor pode variar dependendo da marca do smartphone (Samsung, Xiaomi, Motorola, etc.).
> 
> **A forma mais rápida de encontrar:** Abra o app **Configurações** do seu celular, toque no ícone de **pesquisa (lupa)** no topo da tela e busque por **"Número da versão"** (ou *"Versão do OS"* / *"Versão do MIUI"*).
### Habilitar a Depuração USB
No seu smartphone:

1. Acesse **Configurações → Sobre o telefone**.
2. Toque **7 vezes** sobre **Número da versão** (ou *Build number*) até ativar o modo de desenvolvedor.
3. Volte ao menu principal de configurações e acesse **Opções do desenvolvedor**.
4. Ative a opção **Depuração USB**.

<img width="5760" height="3240" alt="Abra o aplicativo Configurações (Settings) do seu dispositivo Android e deslize até o fim da tela  Toque em Sobre o telefone (About phone)  (2)" src="https://github.com/user-attachments/assets/0ab9bf60-92dd-4ece-95e4-ff26cb83887a" />


<img width="5760" height="3240" alt="Abra o aplicativo Configurações (Settings) do seu dispositivo Android e deslize até o fim da tela  Toque em Sobre o telefone (About phone)  (3)" src="https://github.com/user-attachments/assets/74cc5d3d-48ab-4032-97e7-48fe15eaca3a" />



---

## Verificação da Conexão ADB

1. Conecte o smartphone ao computador via cabo USB.
2. Abra o terminal (PowerShell ou Prompt de Comando) e navegue até a pasta do Platform Tools:

   ```powershell
   cd C:\adb\platform-tools
   ```

3. Execute o comando de verificação:

   ```powershell
   .\adb.exe devices
   ```

> ⚠️ **Atenção (Autorização no Celular):**
> Na primeira vez em que você rodar este comando, aparecerá um **pop-up de confirmação na tela do smartphone** solicitando permissão para a depuração USB. Marque a opção *"Sempre permitir a partir deste computador"* e confirme.

#### Exemplo de saída no terminal:

Ao rodar pela primeira vez (o serviço ADB será iniciado):

```text
PS C:\adb\platform-tools> .\adb.exe devices
* daemon not running; starting now at tcp:5037
* daemon started successfully
List of devices attached
```

Com o dispositivo devidamente autorizado e conectado:

```text
PS C:\adb\platform-tools> .\adb.exe devices
List of devices attached
RXCXXXXXXXX    device 
```

### Validar Permissões de Shell
Para garantir que o computador possui acesso total de comandos ao dispositivo, execute:

```powershell
.\adb.exe shell
```

> 💡 **Nota:** Se o terminal de comandos do Android abrir normalmente (ex: `shell@android:/ $`), a comunicação está funcionando perfeitamente. Digite `exit` para retornar ao PowerShell.

---

##  Dica de Segurança Importante

> 🛡️ **Aviso de Segurança:**
> Sempre que **concluir a coleta de dados, testes ou o uso do ADB**, lembre-se de **desativar as Opções de Desenvolvedor** (ou ao menos desativar a **Depuração USB**) em seu smartphone (**Configurações → Opções do desenvolvedor**).
> 
> Manter o modo de desenvolvedor ou a depuração USB ativos continuamente pode expor seu dispositivo a riscos de segurança caso ele seja conectado a portas USB não confiáveis ou computadores de terceiros.

---

##  Estrutura do Projeto

```text
Projeto/
│
├── scripts/       # Scripts para coleta de dados
├── parsers/       # Processadores dos dados coletados
├── experimentos/  # Diretório de saída (gerado/utilizado para salvar os dados e logs da coleta)
├── docs/          # Documentação detalhada
├── requirements.txt
└── README.md
```

> 💡**Nota sobre a pasta experimentos/:**
> Esta pasta é destinada ao armazenamento automático dos arquivos de saída, logs e resultados gerados durante a execução dos scripts de coleta e dos parsers.

---

##  Próximos Passos

Após finalizar a configuração, consulte as documentações específicas para prosseguir:

* `docs/scripts.md` — Descrição e uso dos scripts de coleta.
* `docs/parsers.md` — Guia de utilização dos *parsers*.
* `docs/experiments.md` — Configuração dos cenários experimentais
