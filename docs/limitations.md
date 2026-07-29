#  Limitações 

Este projeto foi desenvolvido utilizando dispositivos Android e a interface **Android Debug Bridge (ADB)**. Durante o desenvolvimento, foram identificadas limitações inerentes à plataforma que podem afetar a coleta e a análise dos dados. 

Ao final, são apresentadas recomendações de boas práticas para mitigar esses impactos.

---

##  Limitações Identificadas

### 1. Dependência do Fabricante
Os comandos ADB não retornam exatamente as mesmas informações em todos os dispositivos. Fabricantes como Samsung, Motorola, Xiaomi e Google Pixel modificam a implementação dos serviços internos de telefonia, fazendo com que alguns campos estejam ausentes ou possuam nomenclaturas diferentes.
* **Exemplos:**
  * Alguns aparelhos exibem `isNrAvailable`, enquanto outros omitem essa chave;
  * Alguns retornam a lista explícita de bandas LTE/NR, enquanto outros retornam apenas a frequência via `EARFCN` ou `ARFCN`.
  > *Por esse motivo, alguns parsers podem precisar de pequenas adaptações no regex para outros modelos de smartphone.*

---

### 2. Diferenças entre Versões do Android
Atualizações do sistema operacional alteram a estrutura de saída dos comandos nativos (`dumpsys telephony.registry`, `dumpsys telephony.service`, etc.). Campos presentes em uma versão do Android podem ser renomeados ou descontinuados em edições mais recentes.

---

### 3. Permissões e Restrições do Dispositivo
A disponibilidade completa das métricas de rede depende de:
* Modo de Desenvolvedor habilitado;
* Depuração USB ativa e autorizada no computador;
* Ausência de bloqueios de segurança do fabricante/firmware que restrinjam a leitura da RIL (Radio Interface Layer).

---

### 4. Volume de Dados
Comandos contínuos (como `logcat` e dumps de `telephony.registry`) geram um volume massivo de texto em poucos minutos (centenas de milhares de linhas). 
* **Impacto:** Os *parsers* do projeto foram projetados especificamente para filtrar e sumarizar apenas os eventos relevantes de rádio, evitando o estouro de memória e facilitando a análise.

---

### 5. Intervalo entre Coletas
A frequência de amostragem definida no script de coleta influencia diretamente a análise:
* **Intervalos muito curtos:** Geram arquivos gigantescos e aumentam a carga de processamento dos parsers.
* **Intervalos muito longos:** Podem perder transições rápidas da rede (como trocas de célula e flutuações momentâneas de sinal).
> *A escolha da frequência deve ser alinhada ao objetivo específico de cada experimento.*

---

### 6. Dinâmica e Volatilidade da Rede Móvel
Os parâmetros de conexão (banda, Carrier Aggregation, célula atendente, RSRP, 5G NSA/SA) variam constantemente em função de:
* Operadora e carga do setor;
* Localização geográfica e sombreamento de sinal;
* Movimentação do usuário e horário da medição.
* **Nota:** Essas flutuações são comportamentos normais da rede celular e devem ser consideradas durante a análise dos logs.

---

### 7. Sensibilidade dos Parsers ao Formato dos Logs
Os *parsers* utilizam **Expressões Regulares (Regex)** calibradas estritamente para o padrão dos logs gerados pelos scripts deste projeto. Alterações no formato das saídas do Android podem exigir atualização das regras do Regex.

---

### 8. Escopo do Projeto
Este repositório fornece a **infraestrutura de coleta e organização** de parâmetros da camada física e de controle da rede celular via ADB.
* ❌ **Fora de escopo:** Medições de desempenho da camada de aplicação/transporte (como *throughput* de *download/upload*, latência RTT ou perda de pacotes).

---

## 💡 Boas Práticas Recomendadas

Para garantir a **reprodutibilidade** e a **consistência** das coletas em experimentos científicos ou comparativos, recomenda-se:

*  **Padronização de Hardware:** Utilize estritamente o mesmo modelo de smartphone durante todas as etapas do mesmo experimento.
*  **Fixação da Versão do SO:** Mantenha a mesma versão do Android (e da ROM/firmware) ao longo de todas as coletas.
*  **Checklist Pré-Coleta:** Valide o estado da conexão ADB (`adb devices`) antes de iniciar qualquer execução prolongada.
*  **Isolamento de Interferências:** Feche aplicativos em segundo plano que possam consumir dados ou forçar trocas de estado na rede móvel durante os testes.
*  **Validação Imediata:** Execute os *parsers* logo após o encerramento da coleta para confirmar a integridade e a presença de dados no arquivo CSV gerado.
*  **Registro Detalhado do Cenário:** Documente sempre os metadados do teste (local, horário, operadora, tecnologia esperada e condições de mobilidade) no arquivo `metadata.txt` ou na planilha de análise.
