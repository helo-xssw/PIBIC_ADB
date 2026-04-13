## 1. Ambiente Experimental

A coleta de dados foi realizada utilizando um dispositivo móvel Samsung Galaxy A16, com sistema operacional Android 16, compatível com redes móveis 4G (LTE) e 5G. A escolha do dispositivo considerou sua capacidade de acesso a tecnologias recentes de comunicação móvel e sua compatibilidade com o Android Debug Bridge (ADB).

A etapa experimental foi estruturada em duas fases. Inicialmente, a coleta foi conduzida em ambiente controlado de laboratório, com o objetivo de validar os comandos do ADB, compreender o comportamento dos logs gerados e ajustar os parâmetros de coleta. Posteriormente, as coletas serão realizadas em cenário real de uso, incluindo deslocamento do dispositivo, permitindo a análise de variações de sinal, eventos de mobilidade e mudanças de célula em condições práticas.

A região de coleta corresponde ao município de Itacoatiara, no estado do Amazonas, onde há predominância de cobertura 4G (LTE), sendo esta a principal tecnologia considerada nas análises. A tecnologia 5G será incluída nas coletas quando disponível, permitindo análises complementares.

A coleta de dados é realizada de forma passiva, utilizando o Android Debug Bridge (ADB) para captura de logs do sistema, sem interferência no comportamento da rede ou geração artificial de tráfego. Essa abordagem garante maior fidelidade aos dados obtidos.

---

## 2. Dados Coletados

A coleta de dados foi direcionada a informações relevantes para análise de desempenho e comportamento de redes móveis. Para facilitar a compreensão, especialmente por usuários iniciantes, os dados foram organizados em categorias, com explicações sobre seu significado e sua importância na análise.

### 2.1 Métricas de Qualidade do Sinal

| Dado | Significado | Por que coletar? |
|------|------------|------------------|
| RSSI | Indica a intensidade geral do sinal recebido pelo dispositivo | Permite avaliar a força do sinal e identificar áreas com baixa cobertura |
| RSRP | Mede a potência do sinal de referência da rede (mais preciso em 4G/5G) | Fundamental para análise de cobertura e desempenho da rede |
| RSRQ | Indica a qualidade do sinal, considerando interferências | Ajuda a identificar degradação de qualidade mesmo com sinal forte |

---

### 2.2 Estado e Tipo de Conectividade

| Dado | Significado | Por que coletar? |
|------|------------|------------------|
| Tipo de rede (4G/5G) | Indica a tecnologia de rede utilizada pelo dispositivo | Permite comparar desempenho entre diferentes gerações de rede |
| Estado da conexão | Mostra se o dispositivo está conectado ou não à rede | Ajuda a identificar falhas e instabilidade de conexão |

---

### 2.3 Eventos de Rede

| Dado | Significado | Por que coletar? |
|------|------------|------------------|
| Handover | Mudança de uma célula de rede para outra | Importante para análise em movimento e continuidade da conexão |
| Perda de sinal | Momento em que o dispositivo perde conexão com a rede | Indica falhas de cobertura ou instabilidade |
| Reconexão | Retorno da conexão após perda de sinal | Permite avaliar tempo de recuperação da rede |

---

### 2.4 Logs do Subsistema de Rádio

| Dado | Significado | Por que coletar? |
|------|------------|------------------|
| Logs do buffer `radio` | Registros internos do sistema relacionados à rede móvel | Principal fonte de dados para análise de eventos, sinal e comportamento da rede |

---

### 2.5 Dados Complementares

| Dado | Significado | Por que coletar? |
|------|------------|------------------|
| Cell ID | Identificador da célula de rede conectada | Permite rastrear mudanças de célula e localização na rede |
| Estado do serviço | Indica se o dispositivo está em área com cobertura | Ajuda a identificar momentos sem serviço |

---

Para garantir a qualidade da análise, são considerados apenas dados diretamente relacionados ao desempenho e à conectividade da rede móvel. Informações irrelevantes ou redundantes presentes nos logs são descartadas durante o processo de análise.
