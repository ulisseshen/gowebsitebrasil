<!--{
  "Title": "Go Fuzzing technical details",
  "Breadcrumb": true,
  "ia-translated": true
}-->

Este documento fornece uma visão geral dos detalhes técnicos da implementação nativa de fuzzing, e destina-se a ser um recurso para contribuidores.

## Arquitetura geral

O fuzzer usa um único processo coordenador, que gerencia o corpus, e múltiplos processos worker, que mutam entradas e executam o fuzz target. Os processos coordenador e worker se comunicam usando um protocolo RPC baseado em JSON via pipe, e regiões compartilhadas de memória virtual.

Para cada worker, o coordenador cria uma goroutine que spawna o processo worker e configura a comunicação entre processos. Cada goroutine então lê de um canal compartilhado que é alimentado pelo loop principal do coordenador, enviando instruções que lê do canal para os processos worker relevantes.

O loop principal do coordenador escolhe entradas do corpus, enviando-as para o canal compartilhado de workers. Qualquer worker que pegue aquela entrada do canal enviará uma requisição de fuzzing para o processo worker correspondente. Este processo fica em um loop, mutando a entrada e executando o fuzz target até que uma execução cause um aumento nos contadores de cobertura, cause um panic ou crash, ou passe de um prazo predeterminado.

Se o processo worker executa uma entrada mutada que causa um aumento nos contadores de cobertura ou um panic recuperável, ele sinaliza isso ao coordenador que então é capaz de reconstruir a entrada mutada. O coordenador tentará [minimizar a entrada](#input-minimization), então ou adicioná-la ao corpus para fuzzing adicional, no caso de encontrar aumento de cobertura, ou escrevê-la no diretório testdata, no caso de uma entrada que causa um erro ou panic.

Se um erro não recuperável ocorre durante fuzzing que causa o processo worker desligar (por exemplo, loop infinito, os.Exit, exaustão de memória, etc), minimização não será tentada, e a entrada com falha será escrita no diretório testdata e reportada.

<img alt="Diagrama de sequência da interação entre coordenador e worker, conforme descrito acima." src="/security/fuzz/seq-diagram.png"/>

### Comunicação entre processos

Ao spawnar os processos worker filhos, o coordenador configura dois métodos de comunicação: um pipe, que é usado para passar mensagens RPC baseadas em JSON, e uma região de memória compartilhada, que é usada para passar entradas e estado RNG. Cada processo worker tem seu próprio pipe e região de memória compartilhada.

O pipe RPC é usado pelo coordenador para controlar o processo worker, enviando-lhe instruções de fuzzing ou minimização, e pelo worker para repassar resultados de suas operações ao coordenador (isto é, se a entrada expandiu cobertura, causou um crash, foi minimizada com sucesso, etc).

A região de memória compartilhada é usada para passar informações específicas de ida e volta com os workers. O coordenador usa a região para passar a entrada de corpus para fuzz ao worker, e é usada pelo worker para armazenar seu estado RNG atual. O estado RNG é usado pelo coordenador para reconstruir as mutações que foram aplicadas à entrada pelo worker quando ele terminou de executar o target (esta reconstrução acontece tanto quando o worker sai normalmente, quanto quando ele crasheia.)

## Seleção de entrada

O coordenador atualmente não implementa nenhuma forma avançada de priorização de entrada. Ele cicla através de todo o corpus, fazendo loop após esgotar as entradas.

Similarmente, o coordenador não implementa nenhum tipo de minimização de corpus (não deve ser confundido com minimização de entrada, [discutida abaixo](#input-minimization)).

## Orientação de cobertura

O fuzzer usa contadores de cobertura inline de 8 bits [compatíveis com libFuzzer](https://clang.llvm.org/docs/SanitizerCoverage.html#inline-8bit-counters). Esses contadores são inseridos durante a compilação em cada borda de código, e são incrementados na entrada. Contadores não são protegidos contra overflow, para que não fiquem saturados.

Similarmente ao AFL e libFuzzer, ao rastrear cobertura, os contadores são quantizados para a potência de dois mais próxima. Isso permite que o fuzzer diferencie entre mudanças insignificantes e significativas no fluxo de execução. Para rastrear essas mudanças, o fuzzer mantém um slice de bytes que mapeia para os contadores inline, cujos bits indicam se há pelo menos uma entrada no corpus que incrementa o contador relacionado pelo menos 2^bit-position vezes. Esses bytes podem ficar saturados, se houver entradas que fazem contadores atingirem cada valor quantizado, ponto em que o contador relacionado falha em fornecer informações de cobertura úteis adicionais.

Como contadores de cobertura são adicionados a cada borda durante a compilação, código que não está sendo fuzzed também é instrumentado, o que pode fazer com que o worker detecte expansão de cobertura que não está relacionada ao target sendo executado (por exemplo, se algum novo caminho de código é disparado em uma goroutine não relacionada ao fuzz target). O worker tenta reduzir isso de duas maneiras: primeiro ele reseta todos os contadores imediatamente antes de executar o fuzz target e então tira um snapshot dos contadores imediatamente após o target retornar, e segundo ignorando explicitamente um conjunto de packages que provavelmente serão "ruidosos"

Um número de packages explicitamente não têm contadores inseridos, já que é provável que introduzam ruído de contador que não está relacionado ao target sendo executado. Esses packages são:

* `context`
* `internal/fuzz`
* `reflect`
* `runtime`
* `sync`
* `sync/atomic`
* `syscall`
* `testing`
* `time`

## Motor de mutação

Quando o worker recebe uma nova entrada, ele aplica mutações à entrada antes de executar o target com a entrada. Após cada mutação, o fuzz target é executado com a nova entrada, e se a cobertura não for expandida, mutações adicionais são aplicadas. Para evitar que as entradas divirjam massivamente de seu estado inicial, após cinco mutações serem aplicadas a uma entrada, ela é resetada para seu estado original antes que mutações adicionais sejam aplicadas. Por exemplo, para a entrada `hello world`, a estratégia de mutação pode parecer com o seguinte:

```
0. hello world [initial state]
1. kello world [replace first byte]
2. world kello [swap two chunks]
3. world ke    [delete last three bytes]
4. owrld ke    [shuffle first three bytes]
5. owrldx ke   [insert random byte]
6. ello world  [reset to initial state, delete first byte]
...
```

Os mutadores tentam viesar em direção a produzir entradas menores, em vez de entradas maiores, para evitar crescimento rápido do tamanho do corpus.

Há numerosos mutadores para tipos `[]byte` e `string`, e um número menor de mutadores para todos os tipos `int`, `uint`, e `float`.

Atualmente não há estratégias de mutação orientadas por execução implementadas (como correspondência entrada-para-comparação), nem mutadores baseados em dicionário.

## Minimização de entrada

Para evitar que o corpus infle (o que sobrecarrega o fuzzer tanto em termos de desempenho, quanto reduzindo a probabilidade de que uma mutação realmente toque dados interessantes) tentamos minimizar cada entrada descoberta que expande cobertura ou causa um crash recuperável (crashes não recuperáveis, como aqueles causados por exaustão de memória, não são minimizados, pois o processo seria extremamente lento). A estratégia empregada para minimização é bastante simples, tentando sequencialmente remover bytes da entrada enquanto mantém a cobertura inicial encontrada. Em particular, o mecanismo de minimização usa a seguinte estratégia:

1. Tentar cortar um pedaço exponencialmente menor de bytes do final da entrada
2. Tentar remover cada byte individual
3. Tentar remover cada possível subconjunto de bytes
4. Tentar substituir cada byte não legível por humanos por um byte legível por humanos (isto é, algo no conjunto ASCII de bytes)
