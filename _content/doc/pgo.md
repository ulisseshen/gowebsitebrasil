---
ia-translated: true
title: Profile-guided optimization
layout: article
---

A partir do Go 1.20, o compilador Go suporta profile-guided optimization (PGO) para otimizar ainda mais as builds.

Índice:

 [Visão Geral](#overview)\
 [Coletando profiles](#collecting-profiles)\
 [Compilando com PGO](#building)\
 [Notas](#notes)\
 [Perguntas Frequentes](#faq)\
 [Apêndice: fontes alternativas de profile](#alternative-sources)

# Visão Geral {#overview}

Profile-guided optimization (PGO), também conhecida como feedback-directed optimization (FDO), é uma técnica de otimização de compilador que alimenta informações (um profile) de execuções representativas da aplicação de volta ao compilador para a próxima build da aplicação, que usa essas informações para tomar decisões de otimização mais informadas.
Por exemplo, o compilador pode decidir fazer inline mais agressivo de funções que o profile indica serem chamadas frequentemente.

No Go, o compilador usa CPU pprof profiles como entrada de profile, como de [runtime/pprof](https://pkg.go.dev/runtime/pprof) ou [net/http/pprof](https://pkg.go.dev/net/http/pprof).

A partir do Go 1.22, benchmarks para um conjunto representativo de programas Go mostram que compilar com PGO melhora o desempenho em torno de 2-14%.
Esperamos que os ganhos de desempenho geralmente aumentem ao longo do tempo à medida que otimizações adicionais aproveitam o PGO em versões futuras do Go.


# Coletando profiles {#collecting-profiles}

O compilador Go espera um CPU pprof profile como entrada para PGO.
Profiles gerados pelo runtime Go (como de [runtime/pprof](https://pkg.go.dev/runtime/pprof) e [net/http/pprof](https://pkg.go.dev/net/http/pprof)) podem ser usados diretamente como entrada do compilador.
Também pode ser possível usar/converter profiles de outros sistemas de profiling. Veja [o apêndice](#alternative-sources) para informações adicionais.

Para melhores resultados, é importante que os profiles sejam _representativos_ do comportamento real no ambiente de produção da aplicação.
Usar um profile não representativo provavelmente resultará em um binário com pouca ou nenhuma melhoria em produção.
Assim, coletar profiles diretamente do ambiente de produção é recomendado, e é o método principal para o qual o PGO do Go é projetado.

O fluxo de trabalho típico é o seguinte:

1. Compile e lance um binário inicial (sem PGO).
2. Colete profiles da produção.
3. Quando for hora de lançar um binário atualizado, compile do código fonte mais recente e forneça o profile de produção.
4. VÁ PARA 2

O PGO do Go é geralmente robusto a desvios entre a versão perfilada de uma aplicação e a versão sendo compilada com o profile, bem como a compilar com profiles coletados de binários já otimizados.
Isso é o que torna este ciclo de vida iterativo possível.
Veja a seção [AutoFDO](#autofdo) para detalhes adicionais sobre este fluxo de trabalho.

Se for difícil ou impossível coletar do ambiente de produção (por exemplo, uma ferramenta de linha de comando distribuída para usuários finais), também é possível coletar de um benchmark representativo.
Note que construir benchmarks representativos é frequentemente bastante difícil (assim como mantê-los representativos à medida que a aplicação evolui).
Em particular, _microbenchmarks geralmente são maus candidatos para profiling PGO_, pois exercitam apenas uma pequena parte da aplicação, o que gera ganhos pequenos quando aplicado ao programa inteiro.

# Compilando com PGO {#building}

A abordagem padrão para compilar é armazenar um pprof CPU profile com nome de arquivo `default.pgo` no diretório do package main do binário perfilado.
Por padrão, `go build` detectará arquivos `default.pgo` automaticamente e habilitará PGO.

Commitar profiles diretamente no repositório de código é recomendado, pois profiles são uma entrada para a build importante para builds reproduzíveis (e performáticas!).
Armazenar junto com o código simplifica a experiência de build, pois não há etapas adicionais para obter o profile além de buscar o código.

Para cenários mais complexos, a flag `go build -pgo` controla a seleção de profile PGO.
Esta flag tem como padrão `-pgo=auto` para o comportamento `default.pgo` descrito acima.
Definir a flag como `-pgo=off` desabilita completamente as otimizações PGO.

Se você não pode usar `default.pgo` (por exemplo, profiles diferentes para cenários diferentes de um binário, incapaz de armazenar profile com código, etc), você pode passar diretamente um caminho para o profile a usar (por exemplo, `go build -pgo=/tmp/foo.pprof`).

_Nota: Um caminho passado a `-pgo` se aplica a todos os packages main.
por exemplo, `go build -pgo=/tmp/foo.pprof ./cmd/foo ./cmd/bar` aplica `foo.pprof` a ambos os binários `foo` e `bar`, o que frequentemente não é o que você quer.
Geralmente binários diferentes devem ter profiles diferentes, passados via invocações separadas de `go build`._

_Nota: Antes do Go 1.21, o padrão é `-pgo=off`. PGO deve ser habilitado explicitamente._

# Notas {#notes}

## Coletando profiles representativos da produção

Seu ambiente de produção é a melhor fonte de profiles representativos para sua aplicação, como descrito em [Coletando profiles](#collecting-profiles).

A maneira mais simples de começar com isso é adicionar [net/http/pprof](https://pkg.go.dev/net/http/pprof) à sua aplicação e então buscar `/debug/pprof/profile?seconds=30` de uma instância arbitrária do seu serviço.
Esta é uma ótima maneira de começar, mas há maneiras pelas quais isso pode ser não representativo:

* Esta instância pode não estar fazendo nada no momento em que é perfilada, mesmo que geralmente esteja ocupada.

* Padrões de tráfego podem mudar ao longo do dia, fazendo o comportamento mudar ao longo do dia.

* Instâncias podem realizar operações de longa duração (por exemplo, 5 minutos fazendo operação A, depois 5 minutos fazendo operação B, etc).
  Um profile de 30s provavelmente cobrirá apenas um único tipo de operação.

* Instâncias podem não receber distribuições justas de requisições (algumas instâncias recebem mais de um tipo de requisição do que outras).

Uma estratégia mais robusta é coletar múltiplos profiles em diferentes momentos de diferentes instâncias para limitar o impacto de diferenças entre profiles de instâncias individuais.
Múltiplos profiles podem então ser [mesclados](#merging-profiles) em um único profile para uso com PGO.

Muitas organizações executam serviços de "continuous profiling" que realizam este tipo de profiling de amostragem em toda a frota automaticamente, que então poderia ser usado como fonte de profiles para PGO.

## Mesclando profiles {#merging-profiles}

A ferramenta pprof pode mesclar múltiplos profiles assim:

```
$ go tool pprof -proto a.pprof b.pprof > merged.pprof
```

Esta mesclagem é efetivamente uma soma direta de amostras na entrada, independentemente da duração de parede do profile.
Como resultado, ao perfilar uma pequena fatia de tempo de uma aplicação (por exemplo, um servidor que roda indefinidamente), você provavelmente quer garantir que todos os profiles tenham a mesma duração de parede (isto é, todos os profiles são coletados por 30s).
Caso contrário, profiles com maior duração de parede serão sobre-representados no profile mesclado.

## AutoFDO {#autofdo}

O PGO do Go é projetado para suportar um fluxo de trabalho estilo "[AutoFDO](https://research.google/pubs/pub45290/)".

Vamos dar uma olhada mais de perto no fluxo de trabalho descrito em [Coletando profiles](#collecting-profiles):

1. Compile e lance um binário inicial (sem PGO).
2. Colete profiles da produção.
3. Quando for hora de lançar um binário atualizado, compile do código fonte mais recente e forneça o profile de produção.
4. VÁ PARA 2

Isso soa enganosamente simples, mas há algumas propriedades importantes a notar aqui:

* O desenvolvimento está sempre em andamento, então o código fonte da versão perfilada do binário (passo 2) provavelmente é ligeiramente diferente do código fonte mais recente sendo compilado (passo 3).
  O PGO do Go é projetado para ser robusto a isso, o que chamamos de _estabilidade de código_.

* Este é um loop fechado.
  Isto é, após a primeira iteração a versão perfilada do binário já está otimizada com PGO com um profile de uma iteração anterior.
  O PGO do Go também é projetado para ser robusto a isso, o que chamamos de _estabilidade iterativa_.

_Estabilidade de código_ é alcançada usando heurísticas para corresponder amostras do profile ao código sendo compilado.
Como resultado, muitas mudanças no código fonte, como adicionar novas funções, não têm impacto na correspondência de código existente.
Quando o compilador não consegue corresponder código alterado, algumas otimizações são perdidas, mas note que esta é uma _degradação graciosa_.
Uma única função falhando em corresponder pode perder oportunidades de otimização, mas o benefício geral de PGO geralmente está espalhado por muitas funções. Veja a seção [estabilidade de código](#source-stability) para mais detalhes sobre correspondência e degradação.

_Estabilidade iterativa_ é a prevenção de ciclos de desempenho variável em builds PGO sucessivas (por exemplo, build #1 é rápida, build #2 é lenta, build #3 é rápida, etc).
Usamos CPU profiles para identificar funções quentes para direcionar otimizações.
Em teoria, uma função quente poderia ser acelerada tanto pelo PGO que não aparecesse mais como quente no próximo profile e não fosse otimizada, tornando-a lenta novamente.
O compilador Go adota uma abordagem conservadora para otimizações PGO, que acreditamos previne variância significativa.
Se você observar este tipo de instabilidade, por favor registre um issue em [go.dev/issue/new](/issue/new).

Juntas, estabilidade de código e iterativa eliminam o requisito de builds em duas etapas onde uma primeira build não otimizada é perfilada como um canary, e então reconstruída com PGO para produção (a menos que desempenho de pico absoluto seja necessário).

## Estabilidade de código e refatoração {#source-stability}

Como descrito acima, o PGO do Go faz uma tentativa de melhor esforço para continuar correspondendo amostras de profiles mais antigos ao código fonte atual.
Especificamente, Go usa offsets de linha dentro de funções (por exemplo, chamada na 5ª linha da função foo).

Muitas mudanças comuns não quebrarão a correspondência, incluindo:

* Mudanças em um arquivo fora de uma função quente (adicionar/mudar código acima ou abaixo da função).

* Mover uma função para outro arquivo no mesmo package (o compilador ignora completamente nomes de arquivos fonte).

Algumas mudanças que podem quebrar correspondência:

* Mudanças dentro de uma função quente (podem afetar offsets de linha).

* Renomear a função (e/ou tipo para métodos) (muda nome de símbolo).

* Mover a função para outro package (muda nome de símbolo).

Se o profile for relativamente recente, então diferenças provavelmente afetam apenas um pequeno número de funções quentes, limitando o impacto de otimizações perdidas em funções que falham em corresponder.
Ainda assim, degradação se acumulará lentamente ao longo do tempo, já que o código raramente é refatorado _de volta_ para sua forma antiga, então é importante coletar novos profiles regularmente para limitar o desvio de código da produção.

Uma situação onde a correspondência de profile pode degradar significativamente é uma refatoração em grande escala que renomeia muitas funções ou as move entre packages.
Neste caso, você pode ter um impacto de desempenho de curto prazo até que um novo profile mostre a nova estrutura.

Para renomeações mecânicas, um profile existente teoricamente poderia ser reescrito para mudar os nomes de símbolos antigos para os novos nomes.
[github.com/google/pprof/profile](https://pkg.go.dev/github.com/google/pprof/profile) contém os primitivos necessários para reescrever um pprof profile desta forma, mas no momento nenhuma ferramenta pronta para uso existe para isso.

## Desempenho de novo código

Ao adicionar novo código ou habilitar novos caminhos de código com uma flag flip, esse código não estará presente no profile na primeira build, e portanto não receberá otimizações PGO até que um novo profile refletindo o novo código seja coletado.
Tenha em mente ao avaliar o rollout de novo código que o lançamento inicial não representará seu desempenho de estado estável.

# Perguntas Frequentes {#faq}

## É possível otimizar packages da biblioteca padrão Go com PGO?

Sim.
PGO no Go se aplica ao programa inteiro.
Todos os packages são reconstruídos para considerar potenciais otimizações guiadas por profile, incluindo packages da biblioteca padrão.

## É possível otimizar packages em módulos dependentes com PGO?

Sim.
PGO no Go se aplica ao programa inteiro.
Todos os packages são reconstruídos para considerar potenciais otimizações guiadas por profile, incluindo packages em dependências.
Isso significa que a maneira única como sua aplicação usa uma dependência impacta as otimizações aplicadas àquela dependência.

## PGO com um profile não representativo tornará meu programa mais lento do que sem PGO?

Não deveria.
Embora um profile que não seja representativo do comportamento de produção resulte em otimizações em partes frias da aplicação, não deve tornar partes quentes da aplicação mais lentas.
Se você encontrar um programa onde PGO resulta em pior desempenho do que desabilitar PGO, por favor registre um issue em [go.dev/issue/new](/issue/new).

## Posso usar o mesmo profile para diferentes builds GOOS/GOARCH?

Sim.
O formato dos profiles é equivalente entre configurações de OS e arquitetura, então eles podem ser usados entre diferentes configurações.
Por exemplo, um profile coletado de um binário linux/arm64 pode ser usado em uma build windows/amd64.

Dito isso, as ressalvas de estabilidade de código discutidas [acima](#autofdo) se aplicam aqui também.
Qualquer código fonte que difira entre essas configurações não será otimizado.
Para a maioria das aplicações, a vasta maioria do código é independente de plataforma, então degradação desta forma é limitada.

Como exemplo específico, os internals de manipulação de arquivos no package `os` diferem entre Linux e Windows.
Se essas funções forem quentes no profile Linux, os equivalentes Windows não receberão otimizações PGO porque não correspondem aos profiles.

Você pode mesclar profiles de diferentes builds GOOS/GOARCH. Veja a próxima pergunta para os trade-offs de fazer isso.

## Como devo lidar com um único binário usado para diferentes tipos de workload?

Não há escolha óbvia aqui.
Um único binário usado para diferentes tipos de workloads (por exemplo, um banco de dados usado de forma read-heavy em um serviço, e write-heavy em outro serviço) pode ter componentes quentes diferentes, que se beneficiam de otimizações diferentes.

Há três opções:

1. Compile versões diferentes do binário para cada workload: use profiles de cada workload para compilar múltiplas builds específicas para workload do binário.
   Isso fornecerá o melhor desempenho para cada workload, mas pode adicionar complexidade operacional com relação a lidar com múltiplos binários e fontes de profile.

2. Compile um único binário usando apenas profiles do workload "mais importante": selecione o workload "mais importante" (maior footprint, mais sensível a desempenho), e compile usando profiles apenas desse workload.
   Isso fornece o melhor desempenho para o workload selecionado, e provavelmente ainda melhorias modestas de desempenho para outros workloads a partir de otimizações em código comum compartilhado entre workloads.

3. Mescle profiles entre workloads: pegue profiles de cada workload (ponderado por footprint total) e mescle-os em um único profile "fleet-wide" usado para compilar um único profile comum usado para compilar.
   Isso provavelmente fornece melhorias modestas de desempenho para todos os workloads.

## Como PGO afeta o tempo de build?

Habilitar builds PGO provavelmente causará aumentos mensuráveis nos tempos de build de packages.
O componente mais notável disso é que profiles PGO se aplicam a todos os packages em um binário, significando que o primeiro uso de um profile requer uma reconstrução de cada package no grafo de dependências.
Essas builds são armazenadas em cache como qualquer outra, então builds incrementais subsequentes usando o mesmo profile não requerem reconstruções completas.

Se você experimentar aumentos extremos no tempo de build, por favor registre um issue em [go.dev/issue/new](/issue/new).

## Como PGO afeta o tamanho do binário?

PGO pode resultar em binários ligeiramente maiores devido a inlining adicional de funções.

# Apêndice: fontes alternativas de profile {#alternative-sources}

CPU profiles gerados pelo runtime Go (via [runtime/pprof](https://pkg.go.dev/runtime/pprof), etc) já estão no formato correto para uso direto como entradas PGO.
No entanto, organizações podem ter ferramentas alternativas preferidas (por exemplo, Linux perf), ou sistemas existentes de continuous profiling em toda a frota que desejam usar com Go PGO.

Profiles de fontes alternativas podem ser usados com Go PGO se convertidos para o [formato pprof](https://github.com/google/pprof/tree/main/proto), desde que sigam esses requisitos gerais:

* Um dos índices de amostra deve ter tipo/unidade "samples"/"count" ou "cpu"/"nanoseconds".

* Amostras devem representar amostras de tempo de CPU na localização da amostra.

* O profile deve ser simbolizado ([Function.name](https://github.com/google/pprof/blob/76d1ae5aea2b3f738f2058d17533b747a1a5cd01/proto/profile.proto#L208) deve ser definido).

* Amostras devem conter stack frames para funções inlined.
  Se funções inlined forem omitidas, Go não será capaz de manter estabilidade iterativa.

* [Function.start_line](https://github.com/google/pprof/blob/76d1ae5aea2b3f738f2058d17533b747a1a5cd01/proto/profile.proto#L215) deve ser definido.
  Este é o número da linha do início da função.
  isto é, a linha contendo a palavra-chave `func`.
  O compilador Go usa este campo para computar offsets de linha de amostras (`Location.Line.line - Function.start_line`).
  **Note que muitos conversores pprof existentes omitem este campo.**

_Nota: Antes do Go 1.21, metadados DWARF omitem linhas de início de funções (`DW_AT_decl_line`), o que pode tornar difícil para ferramentas determinar a linha de início._

Veja a página [PGO Tools](/wiki/PGO-Tools) no Go Wiki para informações adicionais sobre compatibilidade PGO de ferramentas específicas de terceiros.
