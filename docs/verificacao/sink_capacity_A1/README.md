# Prova de equivalência do adendo A1 (capacidade da bateria do sink)

Porquê e o que muda: `campaign_v2/manifest_addendum_A1.txt`.

Cada pasta contém o `.sca` e o log de uma run de 3600 s, gerada com `run_eq2.sh`:

```
run_eq2.sh <ini> <config> 0 <pasta> \
  --**.sink[*].energyStorage.nominalCapacity=<55J|1500J> \
  --**.sink[*].energyStorage.initialCapacity=<55J|1500J>
```

Cada run calcula dois fingerprints tplx: F_all (todos os módulos) e
F_net (`--fingerprint-modules="not **.sink*.energyStorage"`).

| Pasta | Eventos | F_all | F_net |
|---|---|---|---|
| fp_g35_55J   | 92891808  | 0c77-4f34 | b0b7-0be8 |
| fp_g35_1500J | 92891712  | 4712-cefb | b0b7-0be8 |
| fp_g63_55J   | 157887618 | 1171-9379 | ff95-229e |
| fp_g63_1500J | 157887522 | cc80-54a9 | ff95-229e |

O F_net é idêntico com 55 J e com 1500 J. A diferença de 96 eventos vem do temporizador
`printCapacityStep` (1 % da capacidade nominal) do SimpleEpEnergyStorage do sink, que só
atualiza a capacidade residual.

Comparação dos `.sca`: excluem-se os cabeçalhos de execução, as linhas `param` da opção e o
scalar do `sink[0].energyStorage`. O resultado é 0 linhas de diferença entre 55 J e 1500 J, e
0 linhas entre a run de 55 J e o `.sca` da campanha principal.

```bash
norm() { grep -v -E '^(run |attr (datetime|processid|runId|resultdir)|version |param \*\*\.sink\[\*\]\.energyStorage\.(nominal|initial)Capacity)' "$1" | grep -v 'sink\[0\]\.energyStorage'; }
diff <(norm fp_g35_55J/Grid35_Flooding_Host20-0.sca) <(norm fp_g35_1500J/Grid35_Flooding_Host20-0.sca) && echo idênticos
```
