# Android Mobile Network Data Collection Toolkit

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Android](https://img.shields.io/badge/Android-ADB-green.svg)](https://developer.android.com/studio/command-line/adb)
[![Academic](https://img.shields.io/badge/Research-PIBIC-orange.svg)](#)

Ferramenta desenvolvida em **Python** para automação da coleta, processamento e organização de métricas da camada de acesso de redes móveis (LTE e 5G) utilizando o **Android Debug Bridge (ADB)**.

O projeto foi desenvolvido no âmbito de uma pesquisa de **Iniciação Científica (PIBIC)**, oferecendo uma infraestrutura simples, organizada e extensível para pesquisadores interessados em coletar informações da pilha de telefonia do Android.

---

# Objetivos

- 🔄 **Automatizar** a coleta de informações da rede móvel utilizando comandos ADB, sem necessidade de acesso root.
- 📁 **Organizar** automaticamente os arquivos gerados durante cada experimento.
- 📊 **Processar** logs brutos (`raw.log`) em arquivos estruturados (`.csv`) por meio de parsers desenvolvidos em Python.
- 🔬 **Facilitar** experimentos envolvendo LTE, 5G, Carrier Aggregation, qualidade do sinal e estado da rede.

---

#  Estrutura do Repositório

```text
.
├── scripts/                    # Scripts de coleta via ADB
│   ├── cellinfo.py
│   ├── logcat_radio.py
│   ├── registry.py
│   ├── servicestate.py
│   └── signalstrength.py
│
├── parsers/                    # Parsers para conversão de logs em CSV
│   ├── parse_cellinfo.py
│   ├── parse_logcat_radio.py
│   ├── parse_registry.py
│   ├── parse_servicestate.py
│   └── parse_signalstrength.py
│
├── experiments/                # Diretório de armazenamento das coletas
│   ├── cenario_real/
│   └── laboratorio/
│
├── docs/                       # Documentação do projeto
│   ├── installation.md
│   ├── scripts.md
│   ├── parsers.md
│   ├── experiments.md
│   └── limitations.md
│
├── requirements.txt
└── README.md
```

---

#  Início Rápido

## 1. Pré-requisitos

- Python 3.10 ou superior;
- Android Debug Bridge (ADB) instalado e configurado;
- Smartphone Android com **Depuração USB** habilitada;
- Cabo USB.

---

## 2. Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
```

Acesse a pasta:

```bash
cd SEU_REPOSITORIO
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

> 📖 Consulte `docs/installation.md` para instruções detalhadas de instalação e configuração do ambiente.

---

#  Fluxo de Utilização

## Passo 1 – Verificar a conexão do dispositivo

Conecte o smartphone via USB e confirme que ele foi reconhecido:

```bash
adb devices
```

---

## Passo 2 – Executar uma coleta

Escolha o script correspondente à métrica desejada.

Exemplo:

```bash
python scripts/cellinfo.py
```

Os arquivos serão organizados automaticamente dentro da pasta `experiments/`.

---

## Passo 3 – Processar os dados

Após finalizar a coleta, execute o parser correspondente informando o caminho do arquivo `raw.log`.

Exemplo:

```bash
python parsers/parse_cellinfo.py experiments/cenario_real/cellinfo/2026-05-29_13-02-24/raw.log
```

O arquivo CSV será gerado automaticamente na mesma pasta da coleta.

---

#  Scripts Disponíveis

| Script | Informações coletadas |
|----------|----------------------|
| `cellinfo.py` | Informações da célula servidora e células vizinhas |
| `signalstrength.py` | Intensidade e qualidade do sinal da rede |
| `servicestate.py` | Estado da rede móvel e tecnologias utilizadas |
| `registry.py` | Eventos do Telephony Registry |
| `logcat_radio.py` | Eventos registrados no buffer Radio do Logcat |

---

#  Parsers Disponíveis

| Parser | Arquivo de entrada | Arquivo gerado |
|----------|------------------|----------------|
| `parse_cellinfo.py` | `raw.log` | `cellinfo_parsed.csv` |
| `parse_signalstrength.py` | `raw.log` | `signalstrength_parsed.csv` |
| `parse_servicestate.py` | `raw.log` | `servicestate.csv` |
| `parse_registry.py` | `raw.log` | `registry_parsed.csv` |
| `parse_logcat_radio.py` | `raw.log` | `logcat_radio_parsed.csv` |

---

#  Documentação

A documentação completa encontra-se na pasta `docs/`.

| Documento | Descrição |
|------------|-----------|
| `installation.md` | Instalação e configuração do ambiente |
| `scripts.md` | Descrição dos scripts de coleta e comandos utilizados |
| `parsers.md` | Funcionamento dos parsers e geração dos arquivos CSV |
| `experiments.md` | Organização dos experimentos e estrutura de diretórios |
| `limitations.md` | Limitações conhecidas e boas práticas de utilização |

---

#  Limitações

As informações disponibilizadas pelo Android variam conforme:

- fabricante do dispositivo;
- versão do Android;
- chipset/modem utilizado;
- permissões disponibilizadas pelo sistema.

Por esse motivo, alguns campos podem não estar presentes em todos os dispositivos.

Os scripts e parsers foram desenvolvidos para serem facilmente adaptáveis a diferentes fabricantes e versões do sistema operacional.

Mais informações podem ser encontradas em `docs/limitations.md`.

---

#  Contribuições

Contribuições são bem-vindas.

Caso deseje adicionar novas métricas, comandos ADB ou aprimorar os parsers, sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request*.

---

#  Licença

Este projeto foi desenvolvido para fins acadêmicos no contexto de uma pesquisa de **Iniciação Científica (PIBIC)**.

Caso utilize este repositório em pesquisas ou trabalhos derivados, recomenda-se citar o projeto e seus autores.

