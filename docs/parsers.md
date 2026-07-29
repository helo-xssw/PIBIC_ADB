# Processadores de Logs (Parsers) 

Após a execução dos scripts de coleta, os dados brutos são armazenados no diretório `experiments/`, organizados em pastas por tipo de medição e timestamps com os arquivos `raw.log` e `metadata.txt`.

Os *parsers* (processadores) desenvolvidos neste projeto realizam a extração automática das informações relevantes contidas em `raw.log`, gerando arquivos CSV (`<tipo>_parsed.csv`) no mesmo diretório, prontos para análise em ferramentas como Excel, LibreOffice Calc, Python (Pandas) ou R.

---

##  Estrutura do Diretório `parsers/`

```text
parsers/
│
├── parse_cellinfo.py
├── parse_logcat_radio.py
├── parse_servicestate.py
├── parse_signalstrength.py
└── parse_telephony_registry.py
```

Cada *parser* é especializado em processar o log bruto gerado pelo respectivo script de coleta.

---

##  Como Executar

Antes de executar um *parser*, certifique-se de que a coleta de dados já foi realizada e os arquivos brutos estão organizados.

> ℹ️ **Nota sobre as pastas:** O repositório já inclui as pastas base `experiments/cenario_real/` e `experiments/laboratorio/` organizadas no controle de versão. Ao rodar qualquer script de coleta, o próprio coletor se encarregará de criar automaticamente a subpasta da métrica (ex: `cellinfo/`) e a pasta temporal com a data/hora do teste (`AAAA-MM-DD_HH-MM-SS/`).

### Estrutura Real dos Experimentos

A estrutura de diretórios utilizada pelo projeto segue a organização abaixo (com subpastas criadas automaticamente pelos scripts de coleta contendo `raw.log` e `metadata.txt`):

```text
experiments/
├── cenario_real/
│   ├── cellinfo/
│   │   ├── AAAA-MM-DD_HH-MM-SS/
│   │   │   ├── raw.log
│   │   │   └── metadata.txt
│   │   ├── AAAA-MM-DD_HH-MM-SS/
│   │   └── ...
│   ├── logcat_radio/
│   ├── registry/
│   ├── servicestate/
│   └── signalstrength/
└── laboratorio/
    ├── cellinfo/
    ├── logcat_radio/
    └── ...
```

### Comando Genérico de Execução

Abra o terminal na pasta raiz do projeto e execute indicando o caminho relativo do arquivo `raw.log` (você pode copiar o caminho relativo clicando com o botão direito no arquivo `raw.log` no seu editor de código):

```bash
python parsers/nome_do_parser.py caminho/relativo/para/raw.log
```

---

##  Exemplos Práticos de Uso

### 1. CellInfo
```bash
python parsers/parse_cellinfo.py experiments/cenario_real/cellinfo/AAAA-MM-DD_HH-MM-SS/raw.log
```
> **Saída esperada:** `cellinfo_parsed.csv` (na mesma pasta do log)

---

### 2. ServiceState
```bash
python parsers/parse_servicestate.py experiments/cenario_real/servicestate/AAAA-MM-DD_HH-MM-SS/raw.log
```
> **Saída esperada:** `servicestate.csv`

---

### 3. SignalStrength
```bash
python parsers/parse_signalstrength.py experiments/cenario_real/signalstrength/AAAA-MM-DD_HH-MM-SS/raw.log
```
> **Saída esperada:** `signalstrength_summary.csv`  e `signalstrength_cells.csv`

---

### 4. Registry
```bash
python parsers/parse_telephony_registry.py experiments/cenario_real/registry/AAAA-MM-DD_HH-MM-SS/raw.log
```
> **Saída esperada:** `telephony_min_summary.csv` 

---

### 5. Logcat 
```bash
python parsers/parse_logcat_radio.py experiments/cenario_real/logcat_radio/AAAA-MM-DD_HH-MM-SS/raw.log
```
> **Saída esperada:** `raw_ca.csv`

---

##  Arquivos e Resultados Gerados

Cada parser cria automaticamente seu(s) arquivo(s) CSV exatamente na mesma pasta do arquivo de entrada.

### Exemplo de Estrutura Após o Processamento:

```text
experiments/
└── cenario_real/
    └── cellinfo/
        └── AAAA-MM-DD_HH-MM-SS/
            ├── raw.log
            ├── metadata.txt
            └── cellinfo_parsed.csv  <-- Arquivo CSV gerado pelo parser
```

---

##  Informações Extraídas por Parser



| Parser | Principais Informações Extraídas |
| :--- | :--- |
| **`parse_cellinfo.py`** | Timestamp da coleta, identificadores da célula servidora (PCI, EARFCN, Banda, MCC, MNC, Operadora) e métricas de RF/sinal (RSSI, RSRP, RSRQ, RSSNR, CQI, TA, Level). |
| **`parse_servicestate.py`** | Extrai estado de registro de voz e dados (voice_reg_state, data_reg_state), operadora, tecnologias ativas (voice_rat, data_rat), sinalização de exibição (override_network), suporte a 5G/EN-DC (nr_available, endc_available) e identidade da célula servidora (PCI, EARFCN, Banda). |
| **`parse_signalstrength.py`** | Gera dois CSVs: signalstrength_summary.csv (resumo de RF LTE e 5G NR da célula servidora) e signalstrength_cells.csv (detalhamento célula a célula, incluindo registradas e vizinhas, com PCI, Banda, ARFCN, RSRP, RSRQ e SINR/RSSNR). |
| **`parse_registry.py`** | Consolida o modo de operação (LTE ou LTE+NR_NSA), estado do chip (sim1_in_service), métricas completas de rádio LTE (RSRP, RSRQ, SINR, CQI), identidade LTE (PCI, EARFCN, Banda), métricas de 5G NR (SS-RSRP, SS-RSRQ, SS-SINR) e sinalização de Carrier Aggregation e EN-DC. |
| **`parse_logcat.py`** |Captura eventos de UNSOL_PHYSICAL_CHANNEL_CONFIG e ServiceState, identificando status de Carrier Aggregation (ca_active), contagem de portadoras (num_cells), dados da célula primária (PCell: banda/EARFCN/PCI), células secundárias (SCell: banda/EARFCN), tecnologias ativas (voice_rat, data_rat) e suporte a 5G NR/EN-DC. |

---

## 📌 Observações Importantes

* **Criação Automática de Diretórios:** O *parser* não cria diretórios. Ele espera encontrar um arquivo `raw.log` gerado previamente pelo script de coleta e salva o resultado (`<tipo>_parsed.csv`) no mesmo diretório de origem.
* **Integridade dos Dados:** Os *parsers* realizam apenas a leitura e tratamento dos dados; os arquivos originais `raw.log` e `metadata.txt` nunca são modificados.
* **Logs Vazios ou Incompletos:** Caso o arquivo `raw.log` esteja vazio ou não contenha registros compatíveis, o arquivo CSV será gerado contendo apenas o cabeçalho das colunas.
