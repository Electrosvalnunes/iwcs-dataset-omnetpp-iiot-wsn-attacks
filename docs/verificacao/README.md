# Verificação: contadores de DAO não alteram a simulação

## O que foi verificado
O commit `0515e40` ("RPL: gravar contadores totais de DAO em finish()") adiciona
5 scalars por nó: `daoReceivedCount`, `daoSentCount`, `daoAckReceivedCount`,
`daoForwardedCount` e `daoDroppedCount`. Aqui verifica-se que isso **não altera o
comportamento da rede**. Ou seja, as simulações feitas com esta versão podem ser
comparadas diretamente com as da versão anterior (`60bc5cf`).

## Ambiente
- OMNeT++ 5.7.1, build de release com clang 14 (`~/Downloads/omnetpp-5.7.1`)
- INET 4.2.10 em `OMET57/inet`, com o patch RPL aplicado (commit `62282fd`, tag `ambiente-revisao-v1`)
- `libMAIO_RPL27.so` "antes": `git show 60bc5cf:src/libMAIO_RPL27.so`, sha256 `2bb17799…`
- `libMAIO_RPL27.so` "depois": `git show 0515e40:src/libMAIO_RPL27.so`, sha256 `50bb4369…`
- Entre os dois commits mudam apenas `src/Rpl.cc`, `src/Rpl.h` e a `.so`. Nenhum `.ned` nem `.ini` foi alterado.

## Como
Usou-se [`verificar_fingerprint.sh`](verificar_fingerprint.sh), corrido a partir de `simulations/`. Para cada cenário, com
`omnetpp_RPL_GRID35_NORMAL.ini`, run 0, `sim-time-limit=200s` e Cmdenv:
1. Corre a versão "antes" e obtém o fingerprint de eventos `tplx`
   (instante, módulo, comprimento dos pacotes e dados extra de cada evento).
2. Corre a versão "depois" com `--fingerprint=<valor de antes>`, para que seja o próprio OMNeT++ a verificar.
3. Compara os `.sca` e os `.vec` linha a linha. Só se ignoram os atributos de cabeçalho
   que mudam em todas as execuções: `runId`, `datetime`, `processid` e `resultdir`.

Nos cenários de ataque, `attackStartTime = 100s`, por isso o ataque está ativo
durante metade do teste e o código do ataque é exercitado.

## Resultado: os 3 cenários passaram

| Cenário | Fingerprint `tplx` | Eventos | `.sca` alteradas/removidas | `.sca` adicionadas | `.vec` |
|---|---|---|---|---|---|
| Grid35_Normal | `7fc2-5062` ✔ | 107 290 | 0 | 180 | idêntico |
| Grid35_Blackhole_Host20 | `7e4e-c288` ✔ | 105 321 | 0 | 180 | idêntico |
| Grid35_Wormhole_Host20_Host0 | `03d2-1e60` ✔ | 110 699 | 0 | 180 | idêntico |

As 180 linhas adicionadas são os 5 scalars novos × 36 nós (35 hosts + sink).
Todos os outros scalars e estatísticas (PDR, `endToEndDelay`, `residualEnergyCapacity`,
`rank`, `parentId`, …) são **byte a byte iguais**.

Para referência, ao fim de 200 s:

| Cenário | Pacotes de aplicação recebidos | `parentChanged` pós-warmup | `daoReceived:count` (pós-warmup) |
|---|---|---|---|
| Normal | 78/78 | 0 | 0 |
| Blackhole_Host20 | 51/78 | 2 | 5 |
| Wormhole_Host20_Host0 | 57/78 | 8 | 37 |

## Conteúdo de cada pasta
- `resumo.txt`: o resumo gerado pelo script.
- `antes.log` / `depois.log`: o output do Cmdenv, que inclui o fingerprint.
- `antes.sca` / `depois.sca`: os resultados escalares completos. O atributo `resultdir` aponta
  para uma pasta temporária e não é relevante.
- `sca.diff`: o diff entre os dois `.sca`. Só tem linhas `>`, que são as adicionadas.
- `vec_sha256.txt`: o sha256 dos `.vec`, sem o cabeçalho variável. Os `.vec` não foram
  copiados por causa do tamanho (cerca de 2 MB cada).

## Notas
- O `daoReceived:count` (o `@statistic`) respeita `warmup-period = 80s`. Como os DAO da formação
  da DODAG acontecem entre cerca de 10 s e 34 s, este contador só regista os DAO que ocorrem depois do
  warmup, ou seja, os provocados por mudanças de pai durante os ataques. Os novos `dao*Count` dão o total.
- A config `Grid35_Wormhole_Host20_Host0` cria, de facto, o túnel entre **host[20] e host[3]**
  (o host[0] foi trocado pelo host[3] na versão v5; ver os comentários no `.ini`). O nome da config é histórico.
