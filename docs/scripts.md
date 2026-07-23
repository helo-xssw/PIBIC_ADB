# Scripts de Coleta de Dados 

Este documento apresenta a descrição detalhada dos scripts desenvolvidos em Python para a coleta de dados da rede móvel em dispositivos Android utilizando a interface de comunicação do **Android Debug Bridge (ADB)**.

Cada script é modular e independente, permitindo que o pesquisador/desenvolvedor selecione e execute apenas os coletores necessários para o seu cenário experimental.

---

## Visão Geral dos Scripts

| Script | Comando Base ADB | Foco da Coleta / Informações Principais |
| :--- | :--- | :--- |
| **`cellinfo.py`** | `adb shell dumpsys telephony.registry` | Célula servidora e células vizinhas (*PCI, EARFCN, TAC, CID*) |
| **`servicestate.py`** | `adb shell dumpsys telephony.registry` | Estado da rede, operadora, tecnologia, bandas e *Carrier Aggregation* |
| **`signalstrength.py`** | `adb shell dumpsys telephony.registry` | Métricas e indicadores de intensidade/qualidade de sinal (*LTE / NR*) |
| **`telephony_registry.py`** | `adb shell dumpsys telephony.registry` | Eventos do *framework* Android e alterações diretas de estado de telefonia |
| **`logcat_radio.py`** | `adb logcat -b radio` | Mensagens e eventos em tempo real da camada de rádio (*RIL*) e do *modem* |

---

## Detalhamento dos Scripts

### 1. `cellinfo.py`

#### Comando ADB Utilizado
```bash
adb shell dumpsys telephony.registry
```

#### Descrição
Coleta e organiza informações estruturadas da célula à qual o dispositivo está atualmente conectado (*serving cell*), além de listar dados das células vizinhas (*neighboring cells*) detectadas pelo rádio.

#### Principais Dados Coletados
* **Identificadores Locais:** PCI (*Physical Cell ID*), CID (*Cell ID*), TAC (*Tracking Area Code*).
* **Frequência e Banda:** EARFCN, Banda de Operação.
* **Rede:** MCC (*Mobile Country Code*), MNC (*Mobile Network Code*), Nome da Operadora.
* **Células Vizinhas:** Sinal e identificadores de células adjacentes.

#### Casos de Uso Recomendados
* Mapeamento e identificação da infraestrutura de células atendentes.
* Análise de *handover* (transição de conexão entre células).


---

### 2. `servicestate.py`

#### Comando ADB Utilizado
```bash
adb shell dumpsys telephony.registry
```

#### Descrição
Captura o estado atual do serviço de telefonia do dispositivo, destacando a tecnologia de acesso ativa, recursos avançados da rede e a alocação de canais.

#### Principais Dados Coletados
* **Estado de Conexão:** Estado de registro na rede (*In Service, Out of Service*).
* **Tecnologia de Acesso:** LTE, NR (5G), HSPA, WCDMA, etc.
* **Capacidades Avançadas:** Disponibilidade de *Carrier Aggregation* (CA), suporte a NR Standalone (SA) e Non-Standalone (NSA / EN-DC).
* **Parâmetros da Rede:** Operadora, canal e frequências em uso.

#### Casos de Uso Recomendados
* Monitoramento de disponibilidade da rede 5G (NSA/SA).
* Diagnóstico do uso de *Carrier Aggregation*.
* Avaliação de transições tecnológicas (ex: queda de LTE para 3G/2G) durante deslocamento.

---

### 3. `signalstrength.py`

#### Comando ADB Utilizado
```bash
adb shell dumpsys telephony.registry
```

#### Descrição
Coleta continuamente os indicadores físicos de qualidade e potência de sinal da conexão móvel para tecnologias LTE e 5G NR.

#### Principais Dados Coletados
* **Métricas LTE:**
  * **RSRP** (*Reference Signal Received Power*)
  * **RSRQ** (*Reference Signal Received Quality*)
  * **RSSI** (*Received Signal Strength Indicator*)
  * **RSSNR** (*Reference Signal Signal-to-Noise Ratio*)
  * **CQI** (*Channel Quality Indicator*)
* **Métricas 5G NR** *(quando disponível)*:
  * **SS-RSRP**, **SS-RSRQ** e **SS-SINR**

#### Casos de Uso Recomendados
* Avaliação da qualidade e potência da cobertura de rádio.
* Comparação de desempenho e degradação de sinal entre operadoras.
* Estudos sobre variação de sinal em ambientes internos vs. externos (*indoor/outdoor*).

---

### 4. `telephony_registry.py`

#### Comando ADB Utilizado
```bash
adb shell dumpsys telephony.registry
```

#### Descrição
Monitora e registra em tempo real os eventos disparados pelo serviço central de telefonia do Android (*Telephony Registry*).

#### Principais Dados Coletados
* Alterações no estado de serviço (*Service State*).
* Variações de intensidade de sinal (*Signal Strength*).
* Mudanças no status de conexão de dados (*Data Connection State*).
* Transições no tipo de rede (*Network Type*).

#### Casos de Uso Recomendados
* Acompanhamento temporal da estabilidade da rede durante experimentos de mobilidade.
* Auditoria de reconexões de dados móveis e perda momentânea de sinal.

---

### 5. `logcat_radio.py`

#### Comando ADB Utilizado
```bash
adb logcat -b radio
```

#### Descrição
Captura diretamente do *buffer* de rádio do Android (`logcat -b radio`) todas as mensagens trafegadas pela camada RIL (*Radio Interface Layer*). Diferente dos comandos `dumpsys`, este script realiza uma leitura contínua e em tempo real dos eventos de nível mais baixo acionados pelo *modem*.

#### Principais Dados Coletados
* Configuração de canais físicos (*Physical Channel Configuration*).
* Eventos detalhados de *Carrier Aggregation* e trocas no *modem*.
* Mensagens de estabelecimento/queda de chamadas de dados (*Data Calls*).
* Respostas e comandos de baixo nível enviados via RIL.

#### Casos de Uso Recomendados
* Análises aprofundadas da camada de rádio e comportamento de baixo nível do *modem*.
* Pesquisas avançadas em redes de comunicação móvel que exigem detalhamento no nível de milissegundos.

---

## Guia Rápido de Seleção

Consulte a tabela a seguir para identificar rapidamente qual script utilizar de acordo com a meta do seu teste:

| Objetivo do Experimento | Script Recomendado |
| :--- | :--- |
| Medir e avaliar a **qualidade do sinal** | `signalstrength.py` |
| Mapear a **célula servidora e vizinhas** | `cellinfo.py` |
| Verificar **tecnologia, 5G e agregação de portadoras** | `servicestate.py` |
| Monitorar **mudanças e eventos de estado** na telefonia | `telephony_registry.py` |
| Realizar **análise técnica detalhada da camada de rádio/modem** | `logcat_radio.py` |

---

## Observações Importantes

> 📌 **Execução Independente e Combinada:**  
> Os scripts são totalmente desacoplados. Você pode rodar apenas um script isolado ou executar múltiplos scripts em paralelo em terminais distintos para capturar uma visão completa da rede móvel durante o experimento.

> 📁 **Armazenamento de Dados:**  
> Os dados brutos gerados durante a execução desses scripts serão gravados no diretório `experiments/`. Em seguida, você poderá utilizar os scripts disponíveis na pasta `parsers/` para estruturar e tratar esses logs.
