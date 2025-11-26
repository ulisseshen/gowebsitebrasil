---
title: FIPS 140-3 Compliance
layout: article
ia-translated: true
---

A partir do Go 1.24, binários Go podem operar nativamente em um modo que
facilita a conformidade com FIPS 140-3. Além disso, a toolchain pode compilar contra
versões congeladas dos packages de criptografia que constituem o
Módulo Criptográfico Go.

## FIPS 140-3

NIST FIPS 140-3 é um regime de conformidade do Governo dos EUA para aplicações
de criptografia que entre outras coisas requer o uso de um conjunto de algoritmos
aprovados, e o uso de módulos criptográficos
[CMVP](https://csrc.nist.gov/projects/cryptographic-module-validation-program)-validados
testados nos ambientes operacionais alvo.

Os mecanismos descritos nesta página facilitam a conformidade para aplicações Go.

Aplicações que não têm necessidade de conformidade com FIPS 140-3 podem ignorá-los
com segurança, e não devem habilitar o modo FIPS 140-3.

**NOTA:** Simplesmente usar um módulo criptográfico compatível e validado com FIPS 140-3
pode não—por si só—satisfazer todos os requisitos regulatórios relevantes. A equipe Go não pode fornecer nenhuma
garantia ou suporte sobre como o uso do modo FIPS 140-3 fornecido pode, ou não, satisfazer requisitos regulatórios específicos para usuários
individuais. Deve-se ter cuidado ao determinar se o uso deste módulo satisfaz
seus requisitos específicos.

## O Módulo Criptográfico Go

O Módulo Criptográfico Go é uma coleção de packages da biblioteca padrão Go
sob `crypto/internal/fips140/...` que implementam algoritmos aprovados pelo FIPS 140-3.

Packages de API pública como `crypto/ecdsa` e `crypto/rand` usam transparentemente
o Módulo Criptográfico Go para implementar algoritmos FIPS 140-3.

## Modo FIPS 140-3

A opção de tempo de execução `fips140` [GODEBUG](/doc/godebug) controla se o
Módulo Criptográfico Go opera no modo FIPS 140-3. O padrão é `off`. Não pode
ser alterado após o programa ter iniciado.

Ao operar no modo FIPS 140-3 (a configuração GODEBUG `fips140` é `on`):

 - O Módulo Criptográfico Go executa automaticamente uma auto-verificação de integridade no
   tempo de `init`, comparando o checksum do arquivo objeto do módulo calculado em
   tempo de compilação com os símbolos carregados na memória.

 - Todos os algoritmos executam testes de resposta conhecida (known-answer self-tests) de acordo com a
   Orientação de Implementação FIPS 140-3 relevante, seja no tempo de `init`, ou no primeiro uso.

 - Testes de consistência aos pares são executados em chaves criptográficas geradas.
   Note que isso pode causar uma desaceleração de até 2x para certos tipos de chave, o que
   é especialmente relevante para chaves efêmeras.

 - [`crypto/rand.Reader`](/pkg/crypto/rand/#Reader) é implementado em termos de um
   DRBG NIST SP 800-90A. Para garantir o mesmo nível de segurança que
   `GODEBUG=fips140=off`, bytes aleatórios também são obtidos do CSPRNG da plataforma a
   cada `Read` e misturados na saída como dados adicionais não creditados.

 - O package [`crypto/tls`](/pkg/crypto/tls/) irá ignorar e não negociar
   nenhuma versão de protocolo, conjunto de cifras, algoritmo de assinatura ou mecanismo de troca
   de chave que não seja aprovado pelo FIPS 140-3.

 - [`crypto/rsa.SignPSS`](/pkg/crypto/rsa/#SignPSS) com
   [`PSSSaltLengthAuto`](/pkg/crypto/rsa/#PSSSaltLengthAuto) irá limitar o comprimento
   do salt ao comprimento do hash.

Quando `GODEBUG=fips140=only` é usado, além do acima, algoritmos
criptográficos que não são compatíveis com FIPS 140-3 retornarão um erro ou panic. Note
que este modo é um esforço de melhor intenção e não pode garantir conformidade com todos os
requisitos FIPS 140-3.

`GODEBUG=fips140=on` e `only` não são suportados em plataformas OpenBSD, Wasm, AIX e
Windows de 32 bits.

## O package `crypto/fips140`

A função [`crypto/fips140.Enabled`](/pkg/crypto/fips140/#Enabled) reporta
se o modo FIPS 140-3 está ativo.

## A variável de ambiente `GOFIPS140`

A variável de ambiente `GOFIPS140` pode ser usada com `go build`, `go install`,
e `go test` para selecionar a versão do Módulo Criptográfico Go a ser vinculada
ao programa executável.

 - `off` é o padrão, e usa os packages `crypto/internal/fips140/...` na
   árvore da biblioteca padrão em uso.

 - `latest` é como `off`, mas habilita o modo FIPS 140-3 por padrão.

 - `v1.0.0` usa o Módulo Criptográfico Go versão v1.0.0, congelado no início de 2025
   e lançado pela primeira vez com o Go 1.24. Ele habilita o modo FIPS 140-3 por padrão.

## Validações de Módulo

O Google atualmente tem uma relação contratual com [Geomys](https://geomys.org/)
para facilitar validações CMVP anuais do Módulo Criptográfico Go.
No momento da validação, vamos congelar o Módulo Criptográfico Go e criar
uma nova versão de módulo para submissão.

Essas validações são testadas em um conjunto abrangente de Ambientes
Operacionais, suportando muitas combinações populares de sistema operacional e plataforma
de hardware.

Validações fora de ciclo podem ser realizadas se problemas de segurança forem descobertos
no módulo.

###  Versões de Módulo Validadas

Lista de versões de módulo que completaram [validação CMVP](https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search?SearchMode=Basic&ModuleName=Go+Cryptographic+Module&CertificateStatus=Active&ValidationYear=0):

_Atualmente não há versões de módulo que completaram a validação._

### Versões de Módulo Em Processo

Lista de versões de módulo que estão atualmente na [Lista de Módulos Em Processo do CMVP](https://csrc.nist.gov/Projects/cryptographic-module-validation-program/modules-in-process/modules-in-process-list):

* v1.0.0 ([Certificado CAVP A6650](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/details?validation=39260)), Revisão Pendente, disponível no Go 1.24+

### Versões de Módulo de Implementação Sob Teste

Lista de versões de módulo que estão atualmente na [Lista de Implementação Sob Teste do CMVP](https://csrc.nist.gov/Projects/cryptographic-module-validation-program/modules-in-process/iut-list):

_Atualmente não há versões de módulo sob teste._

## Go+BoringCrypto

O mecanismo anterior, sem suporte, para usar o módulo BoringCrypto para certos
algoritmos aprovados pelo FIPS 140-3 ainda está disponível atualmente, mas está planejado para
ser removido e substituído pelo mecanismo descrito nesta página em um
release futuro.

Go+BoringCrypto é incompatível com o modo FIPS 140-3 nativo.
