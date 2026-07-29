# Experimentos

Este documento descreve como os dados brutos e processados são organizados no diretório `experiments/` do repositório, além de fornecer orientações para a realização de novos experimentos e para a reprodução das coletas.

---

# Estrutura do diretório `experiments`

Os scripts de coleta foram desenvolvidos para organizar automaticamente os arquivos gerados durante cada execução.

A estrutura recomendada é a seguinte:

```text
experiments/
├── cenario_real/
│   ├── cellinfo/
│   │   ├── AAAA-MM-DD_HH-MM-SS/
│   │       ├── raw.log
│   │       ├── metadata.txt
│   │       └── cellinfo_parsed.csv
│   │
│   ├── logcat_radio/
│   ├── registry/
│   ├── servicestate/
│   └── signalstrength/
│
└── laboratorio/
    ├── cellinfo/
    ├── logcat_radio/
    ├── registry/
    ├── servicestate/
    └── signalstrength/
```

Cada métrica possui seu próprio diretório e cada execução gera uma nova pasta identificada pela data e horário da coleta.

---

# Conteúdo de cada coleta

Cada pasta de execução contém os arquivos gerados durante um experimento.

Exemplo:

```text
2026-05-29_13-02-24/
├── raw.log
├── metadata.txt
└── cellinfo_parsed.csv
```

## Arquivos

**`raw.log`**

Contém o log bruto obtido diretamente pelo comando ADB.

Este arquivo nunca deve ser modificado, pois representa a coleta original.

---

**`metadata.txt`**

Armazena informações sobre o contexto da coleta, como dispositivo, operadora e cenário experimental.

---

**`<metrica>_parsed.csv`**

Arquivo gerado após a execução do parser correspondente.

Contém apenas as informações relevantes extraídas do `raw.log`, organizadas em formato tabular para facilitar análises posteriores.

---

# Fluxo recomendado de trabalho

Para cada experimento recomenda-se seguir a sequência abaixo.

1. Conectar o smartphone via USB.
2. Verificar a conexão utilizando:

```bash
adb devices
```

3. Escolher o cenário da coleta (`cenario_real`, `laboratorio` ou outro).
4. Executar o script de coleta desejado.
5. Encerrar a coleta.
6. Executar o parser correspondente informando o caminho do `raw.log`.
7. Verificar se o arquivo `.csv` foi gerado corretamente.

---

# Registro do experimento

Para facilitar a organização e garantir a reprodutibilidade, recomenda-se preencher o arquivo `metadata.txt` com informações da coleta.

| Campo | Exemplo |
|--------|---------|
| Data e Hora | 29/05/2026 - 13:02:24 |
| Cenário | cenario_real |
| Métrica | cellinfo |
| Operadora | Vivo |
| Dispositivo | Samsung Galaxy S23 FE |
| Android | Android 14 |

Essas informações permitem identificar as condições em que os dados foram coletados.

---

# Adaptabilidade dos scripts

Os scripts disponibilizados neste repositório foram desenvolvidos para atender aos experimentos desta pesquisa, mas podem ser modificados conforme a necessidade de novos estudos.

É possível, por exemplo:

- alterar o intervalo entre as coletas;
- adicionar novos comandos ADB;
- criar novos scripts para outras métricas;
- modificar o formato dos arquivos gerados.

Dessa forma, o repositório pode ser utilizado como base para diferentes tipos de experimentos envolvendo redes móveis.

---

# Adaptabilidade dos parsers

Os parsers também podem ser facilmente adaptados para diferentes dispositivos ou objetivos de pesquisa.

Algumas possibilidades incluem:

- adicionar novos campos utilizando Expressões Regulares (Regex);
- capturar informações específicas de determinados fabricantes;
- exportar apenas colunas de interesse;
- calcular métricas adicionais diretamente durante o processamento.

Caso o formato do log seja alterado, normalmente basta atualizar as expressões regulares utilizadas pelo parser.

---

# Armazenamento dos resultados

Os arquivos possuem funções diferentes durante o processo de análise.

| Arquivo | Finalidade |
|----------|------------|
| `raw.log` | Dados brutos coletados pelo ADB |
| `metadata.txt` | Informações do experimento |
| `*_parsed.csv` | Dados estruturados para análise |

Recomenda-se manter todos esses arquivos durante o desenvolvimento da pesquisa.

Os arquivos `.log` permitem que novos parsers sejam executados futuramente sem a necessidade de repetir toda a coleta.

---

# Reprodutibilidade

Para facilitar a reprodução dos experimentos por outros pesquisadores, recomenda-se:

- utilizar o mesmo dispositivo durante uma campanha de coleta;
- registrar a versão do Android;
- registrar a operadora utilizada;
- manter os arquivos `raw.log`;
- documentar alterações realizadas nos scripts ou nos parsers;
- manter a estrutura de diretórios do repositório.

Essas práticas tornam os experimentos mais organizados e facilitam comparações entre diferentes campanhas de coleta.
