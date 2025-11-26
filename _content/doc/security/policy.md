---
title: Go Security Policy
layout: article
breadcrumb: true
ia-translated: true
---

## Visão Geral

Este documento explica o processo da equipe de Segurança do Go para lidar com problemas
reportados e o que esperar em retorno.

## Reportando um Bug de Segurança

Todos os bugs de segurança na distribuição Go devem ser reportados por email para
[security@golang.org](mailto:security@golang.org). Este email é entregue para
a equipe de Segurança do Go.

Para garantir que seu relatório não seja marcado como spam, **por favor inclua a palavra
"vulnerability"** em qualquer lugar no seu email. Por favor use uma linha de assunto descritiva
para seu email de relatório.

Seu email será reconhecido dentro de 7 dias, e você será mantido atualizado
com o progresso até a resolução. Seu problema será corrigido ou tornado público
dentro de 90 dias.

Se você não recebeu uma resposta ao seu email dentro de 7 dias, por favor acompanhe
com a equipe de Segurança do Go novamente em
[security@golang.org](mailto:security@golang.org). Por favor certifique-se de que a palavra
**vulnerability** está no seu email.

Se após mais 3 dias você ainda não recebeu um reconhecimento do seu
relatório, é possível que seu email tenha sido marcado como spam. Nesse
caso, por favor [abra um issue aqui](https://g.co/vulnz). Selecione _"I want to
report a technical security or an abuse risk related bug in a Google product
(SQLi, XSS, etc.)"_, e liste _"Go"_ como o produto afetado.

## Categorias

Dependendo da natureza do seu problema, ele será categorizado pela equipe de
Segurança do Go como um problema na categoria PUBLIC, PRIVATE, ou URGENT. Todos os problemas de segurança
receberão números CVE.

A equipe de Segurança do Go não atribui rótulos de severidade tradicionais de granularidade fina
(ex. CRITICAL, HIGH, MEDIUM, LOW) para problemas de segurança porque a severidade depende
altamente de como um usuário está usando a API ou funcionalidade afetada.

Por exemplo, o impacto de um problema de exaustão de recursos no parser `encoding/json`
depende do que está sendo analisado. Se o usuário está analisando arquivos JSON confiáveis
do seu sistema de arquivos local, o impacto provavelmente será baixo. Se o usuário
está analisando JSON arbitrário não confiável de um corpo de requisição HTTP, o impacto pode ser
muito maior.

Dito isso, as seguintes categorias de problemas sinalizam quão severo e/ou de amplo alcance
a equipe de Segurança acredita que um problema é. Por exemplo, um problema com impacto médio a
significativo para muitos usuários é um problema de categoria PRIVATE nesta política, e
um problema com impacto negligenciável a menor, ou que afeta apenas um pequeno subconjunto
de usuários, é um problema de categoria PUBLIC.

### PUBLIC

Problemas na categoria PUBLIC afetam configurações de nicho, têm impacto muito limitado,
ou já são amplamente conhecidos.

Problemas de categoria PUBLIC são rotulados com
[`Proposal-Security`](https://github.com/golang/go/labels/Proposal-Security),
discutidos através do
[processo de revisão de propostas do Go](https://go.googlesource.com/proposal/+/master/README.md#proposal-review)
**corrigidos em público**, e portados para os próximos [releases
minor](/wiki/MinorReleases) agendados (que ocorrem ~mensalmente). O anúncio de release
inclui detalhes desses problemas, mas não há pré-anúncio.

Exemplos de problemas PUBLIC passados incluem:

- [#44916](/issue/44916): archive/zip: can panic when calling Reader.Open
- [#44913](/issue/44913): encoding/xml: infinite loop when using xml.NewTokenDecoder with a custom TokenReader
- [#43786](/issue/43786): crypto/elliptic: incorrect operations on the P-224 curve
- [#40928](/issue/40928): net/http/cgi,net/http/fcgi: Cross-Site Scripting (XSS) when Content-Type is not specified
- [#40618](/issue/40618): encoding/binary: ReadUvarint and ReadVarint can read an unlimited number of bytes from invalid inputs
- [#36834](/issue/36834): crypto/x509: certificate validation bypass on Windows 10

### PRIVATE

Problemas na categoria PRIVATE são violações de propriedades de segurança comprometidas.

Problemas de categoria PRIVATE são **corrigidos nos próximos [releases
minor](/wiki/MinorReleases) agendados**, e são mantidos privados até então.

Três a sete dias antes do release, um pré-anúncio é enviado para
golang-announce, anunciando a presença de uma ou mais correções de segurança nos
releases futuros, e se os problemas afetam a biblioteca padrão, a
toolchain, ou ambos, bem como IDs CVE reservados para cada uma das correções.

Para problemas que estão presentes em um [release candidate de versão major](/s/release),
seguimos o mesmo processo, incluindo correções no próximo release
candidate agendado.

Alguns exemplos de problemas PRIVATE passados incluem:

- [#53416](/issue/53416): path/filepath: stack exhaustion in Glob
- [#53616](/issue/53616): go/parser: stack exhaustion in all Parse* functions
- [#54658](/issue/54658): net/http: handle server errors after sending GOAWAY
- [#56284](/issue/56284): syscall, os/exec: unsanitized NUL in environment variables

### URGENT

Problemas de categoria URGENT são uma ameaça à integridade do ecossistema Go, ou estão sendo
ativamente explorados em campo levando a danos graves. Não há exemplos
recentes, mas eles incluiriam execução remota de código em net/http, ou
recuperação prática de chave em crypto/tls.

Problemas de categoria URGENT são corrigidos em privado, e **disparam um
release de segurança dedicado imediato**, possivelmente sem pré-anúncio.

## Sinalizando Issues Existentes como Relacionados a Segurança

Se você acredita que um [issue existente](/issue) está relacionado a segurança, pedimos
que você envie um email para [security@golang.org](mailto:security@golang.org).
O email deve incluir o ID do issue e uma breve descrição de por que ele deve
ser tratado de acordo com esta política de segurança.

## Processo de Divulgação

O projeto Go usa o seguinte processo de divulgação:

1. Uma vez que o relatório de segurança é recebido, ele é atribuído a um manipulador primário. Esta
pessoa coordena o processo de correção e release.

2. O problema é confirmado e uma lista de software afetado é determinada.

3. O código é auditado para encontrar quaisquer problemas similares potenciais.

4. Se for determinado, em consulta com o submissor, que um número CVE
é necessário, o manipulador primário obterá um.

5. Correções são preparadas para as duas versões major mais recentes e a
revisão head/master. Correções são preparadas para as duas versões major mais recentes
e mescladas para head/master.

6. Na data em que as correções são aplicadas, anúncios são enviados para
[golang-announce](https://groups.google.com/group/golang-announce),
[golang-dev](https://groups.google.com/group/golang-dev), e
[golang-nuts](https://groups.google.com/group/golang-nuts).

Este processo pode levar algum tempo, especialmente quando coordenação é necessária com
mantenedores de outros projetos. Todo esforço será feito para lidar com o bug de
maneira tão oportuna quanto possível, no entanto é importante que sigamos o
processo descrito acima para garantir que divulgações sejam tratadas consistentemente.

Para problemas de segurança que incluem a atribuição de um número CVE, o problema é
listado publicamente sob o
["produto Golang" no site CVEDetails](https://www.cvedetails.com/vulnerability-list/vendor_id-14185/Golang.html)
bem como no
[site National Vulnerability Disclosure](https://web.nvd.nist.gov/view/vuln/search).

## Recebendo Atualizações de Segurança

A melhor maneira de receber anúncios de segurança é inscrever-se na
lista de email [golang-announce](https://groups.google.com/forum/#!forum/golang-announce).
Quaisquer mensagens pertinentes a um problema de segurança serão prefixadas com
`[security]`.

## Comentários sobre Esta Política

Se você tiver sugestões para melhorar esta política, por favor
[abra um issue](/issue/new) para discussão.
