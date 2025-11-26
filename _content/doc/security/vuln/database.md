---
title: Go Vulnerability Database
layout: article
ia-translated: true
---

[Voltar para Gerenciamento de Vulnerabilidades do Go](/security/vuln)

## Visão Geral

O banco de dados de vulnerabilidades do Go ([https://vuln.go.dev](https://vuln.go.dev))
serve informações de vulnerabilidade do Go no
[schema Open Source Vulnerability (OSV)](https://ossf.github.io/osv-schema/).

Você também pode navegar pelas vulnerabilidades no banco de dados em [pkg.go.dev/vuln](https://pkg.go.dev/vuln).

**Não** confie no conteúdo do repositório Git x/vulndb. Os arquivos YAML naquele
repositório são mantidos usando um formato interno que pode mudar
sem aviso.

## Contribuindo

Adoraríamos que todos os mantenedores de packages Go [contribuíssem](/s/vulndb-report-new)
informações sobre vulnerabilidades públicas em seus próprios projetos,
e [atualizassem](/s/vulndb-report-feedback) informações existentes sobre vulnerabilidades
em seus packages Go.

Visamos tornar o processo de relatório de baixa fricção,
então sinta-se à vontade para [nos enviar suas sugestões](/s/vuln-feedback).

Por favor **não** use os formulários acima para reportar uma vulnerabilidade na
biblioteca padrão do Go ou sub-repositórios.
Em vez disso, siga o processo em [go.dev/security/policy](/security/policy)
para vulnerabilidades sobre o projeto Go.

## API

O banco de dados canônico de vulnerabilidades do Go, [https://vuln.go.dev](https://vuln.go.dev),
é um servidor HTTP que pode responder a requisições GET para os endpoints especificados abaixo.

Os endpoints não têm parâmetros de query, e nenhum header específico é necessário.
Por causa disso, até mesmo um site servindo de um sistema de arquivos fixo (incluindo uma URL `file://`)
pode implementar esta API.

Cada endpoint retorna uma resposta codificada em JSON, seja em forma descompactada
(se requisitado como `.json`) ou em forma gzipada (se requisitado como `.json.gz`).

Os endpoints são:

- `/index/db.json[.gz]`

  Retorna metadados sobre o banco de dados:

  ```json
  {
    // O último momento em que o banco de dados deve ser considerado
    // como tendo sido modificado, como um timestamp UTC formatado em RFC3339
    // terminando em "Z".
    "modified": string
  }
  ```

  Note que o tempo modificado *não deve* ser comparado com o tempo do relógio de parede,
  por exemplo, para propósitos de invalidação de cache, pois pode haver um atraso em tornar
  modificações do banco de dados públicas.

  Veja [/index/db.json](https://vuln.go.dev/index/db.json) para um exemplo ao vivo.

- `/index/modules.json[.gz]`

  Retorna uma lista contendo metadados sobre cada módulo no banco de dados:

  ```json
  [ {
    // O caminho do módulo.
    "path": string,
    // As vulnerabilidades que afetam este módulo.
    "vulns":
      [ {
        // O ID da vulnerabilidade.
        "id": string,
        // O último momento em que a vulnerabilidade deve ser considerada
        // como tendo sido modificada, como um timestamp UTC formatado em RFC3339
        // terminando em "Z".
        "modified": string,
        // (Opcional) A versão do módulo (no formato SemVer 2.0.0)
        // que contém a última correção para a vulnerabilidade.
        // Se desconhecido ou indisponível, isto deve ser omitido.
        "fixed": string,
      } ]
  } ]
  ```

  Veja [/index/modules.json](https://vuln.go.dev/index/modules.json) para um exemplo ao vivo.

- `/index/vulns.json[.gz]`

  Retorna uma lista contendo metadados sobre cada vulnerabilidade no banco de dados:

  ```json
   [ {
       // O ID da vulnerabilidade.
       "id": string,
       // O último momento em que a vulnerabilidade deve ser considerada
       // como tendo sido modificada, como um timestamp UTC formatado em RFC3339
       // terminando em "Z".
       "modified": string,
       // Uma lista de IDs da mesma vulnerabilidade em outros bancos de dados.
       "aliases": [ string ]
   } ]
  ```

  Veja [/index/vulns.json](https://vuln.go.dev/index/vulns.json) para um exemplo ao vivo.

- `/ID/$id.json[.gz]`

  Retorna o relatório individual para a vulnerabilidade com ID `$id`,
  no formato OSV (descrito abaixo em [Schema](#schema)).

  Veja [/ID/GO-2022-0191.json](https://vuln.go.dev/ID/GO-2022-0191.json)
  para um exemplo ao vivo.

### Download em massa

Para facilitar o download do banco de dados completo de vulnerabilidades do Go,
um arquivo zip contendo todos os arquivos de índice e OSV está disponível em
[vuln.go.dev/vulndb.zip](https://vuln.go.dev/vulndb.zip).

### Uso em `govulncheck`

Por padrão, `govulncheck` usa o banco de dados canônico de vulnerabilidades do Go em [vuln.go.dev](https://vuln.go.dev).

O comando pode ser configurado para contatar um banco de dados de vulnerabilidades diferente usando a flag `-db`, que aceita uma URL de banco de dados de vulnerabilidades com protocolo `http://`, `https://`, ou `file://`.

Para funcionar corretamente com `govulncheck`, o banco de dados de vulnerabilidades especificado deve implementar a API descrita acima. O comando `govulncheck` usa endpoints comprimidos ".json.gz" ao ler de uma fonte http(s), e os endpoints ".json" ao ler de uma fonte file.

### API Legada

O banco de dados canônico contém alguns endpoints adicionais que fazem parte de uma API legada.
Planejamos remover o suporte para esses endpoints em breve. Se você está confiando na API legada
e precisa de tempo adicional para migrar, [por favor nos avise](/s/govulncheck-feedback).

## Schema

Relatórios usam o
[schema Open Source Vulnerability (OSV)](https://ossf.github.io/osv-schema/).
O banco de dados de vulnerabilidades do Go atribui os seguintes significados aos campos:

### id

O campo id é um identificador único para a entrada de vulnerabilidade. É uma string
no formato GO-\<ANO>-\<ENTRYID>.

### affected

O campo [affected](https://ossf.github.io/osv-schema/#affected-fields) é um
array JSON contendo objetos que descrevem as versões de módulo que contêm
a vulnerabilidade.

#### affected[].package

O campo
[affected[].package](https://ossf.github.io/osv-schema/#affectedpackage-field)
é um objeto JSON identificando o _módulo_ afetado. O objeto tem dois
campos obrigatórios:

- **ecosystem**: este sempre será "Go"
- **name**: este é o caminho do módulo Go
  - Packages importáveis na biblioteca padrão terão o nome _stdlib_.
  - O comando go terá o nome _toolchain_.

#### affected[].ecosystem_specific

O campo
[affected[].ecosystem_specific](https://ossf.github.io/osv-schema/#affectedecosystem_specific-field)
é um objeto JSON com informações adicionais sobre a vulnerabilidade,
que é usado pelas ferramentas de detecção de vulnerabilidade do Go.

Por enquanto, ecosystem specific sempre será um objeto com um único campo,
`imports`.

##### affected[].ecosystem_specific.imports

O campo `affected[].ecosystem_specific.imports` é um array JSON contendo
os packages e símbolos afetados pela vulnerabilidade. Cada objeto no
array terá esses dois campos:

- **path:** uma string com o caminho de importação do package contendo a vulnerabilidade
- **symbols:** um array de strings com os nomes dos símbolos (função ou método) que contém a vulnerabilidade
- **goos**: um array de strings com o sistema operacional de execução onde os símbolos aparecem, se conhecido
- **goarch**: um array de strings com a arquitetura onde os símbolos aparecem, se conhecido

### database_specific

O campo `database_specific` contém campos customizados específicos ao banco de dados de vulnerabilidades do Go.

#### database_specific.url

O campo `database_specific.url` é uma string representando a
URL totalmente qualificada do relatório de vulnerabilidade do Go, por exemplo, "https://pkg.go.dev/vuln/GO-2023-1621".

#### database_specific.review_status

O campo `database_specific.review_status` é uma string representando o status de revisão
do relatório de vulnerabilidade. Se não estiver presente, o relatório deve ser
considerado `REVIEWED`. Os valores possíveis são:

- `UNREVIEWED`: O relatório foi gerado automaticamente com base em outra fonte, como
um CVE ou GHSA. Seus dados podem ser limitados e não foram verificados pela equipe Go.
- `REVIEWED`: O relatório se originou da equipe Go, ou foi gerado com base em uma fonte externa.
Um membro da equipe Go revisou o relatório, e onde apropriado, adicionou dados adicionais.

Para informações sobre outros campos no schema, consulte a [especificação OSV](https://ossf.github.io/osv-schema).

## Nota sobre Versões

Nossas ferramentas tentam mapear automaticamente módulos e versões em
avisos de fonte para módulos e versões Go canônicos, de acordo com
os [números de versão de módulo Go](/doc/modules/version-numbers) padrão. Ferramentas como
`govulncheck` são projetadas para confiar nessas versões padrão para determinar
se um projeto Go é afetado por uma vulnerabilidade em uma dependência ou não.

Em alguns casos, como quando um projeto Go usa seu próprio esquema de versionamento,
o mapeamento para versões padrão Go pode falhar. Quando isso acontece, o
relatório do banco de dados de vulnerabilidades do Go pode conservadoramente listar todas as versões Go como
afetadas. Isso garante que ferramentas como `govulncheck` não deixem de reportar
vulnerabilidades devido a faixas de versão não reconhecidas (falsos negativos).
No entanto, listar conservadoramente todas as versões como afetadas pode fazer com que as ferramentas
incorretamente reportem uma versão corrigida de um módulo como contendo a vulnerabilidade
(falsos positivos).

Se você acredita que `govulncheck` está incorretamente reportando (ou deixando de reportar) uma
vulnerabilidade, por favor
[sugira uma edição](https://github.com/golang/vulndb/issues/new?assignees=&labels=Needs+Triage%2CSuggested+Edit&template=suggest_edit.yaml&title=x%2Fvulndb%3A+suggestion+regarding+GO-2024-2965&report=GO-XXXX-YYYY)
ao relatório de vulnerabilidade e nós iremos revisá-lo.

## Exemplos

Todas as vulnerabilidades no banco de dados de vulnerabilidades do Go usam o schema OSV
descrito acima.

Veja os links abaixo para exemplos de diferentes vulnerabilidades Go:

- **Vulnerabilidade na biblioteca padrão Go** (GO-2022-0191):
  [JSON](https://vuln.go.dev/ID/GO-2022-0191.json),
  [HTML](https://pkg.go.dev/vuln/GO-2022-0191)
- **Vulnerabilidade na toolchain Go** (GO-2022-0189):
  [JSON](https://vuln.go.dev/ID/GO-2022-0189.json),
  [HTML](https://pkg.go.dev/vuln/GO-2022-0189)
- **Vulnerabilidade em módulo Go** (GO-2020-0015):
  [JSON](https://vuln.go.dev/ID/GO-2020-0015.json),
  [HTML](https://pkg.go.dev/vuln/GO-2020-0015)

## Relatórios Excluídos

Os relatórios no banco de dados de vulnerabilidades do Go são coletados de diferentes
fontes e curados pela equipe de Segurança do Go. Podemos nos deparar com um aviso de vulnerabilidade
(por exemplo, um CVE ou GHSA) e optar por excluí-lo por várias razões.
Nesses casos, um relatório mínimo será criado no repositório x/vulndb,
sob
[x/vulndb/data/excluded](https://github.com/golang/vulndb/tree/master/data/excluded).

Relatórios podem ser excluídos por estas razões:

- `NOT_GO_CODE`: A vulnerabilidade não está em um package Go,
  mas foi marcada como um aviso de segurança para o ecossistema Go por outra fonte.
  Esta vulnerabilidade não pode afetar nenhum
  package Go. (Por exemplo, uma vulnerabilidade em uma biblioteca C++.)
- `NOT_IMPORTABLE`: A vulnerabilidade ocorre no package `main`, um package `internal/`
  importado apenas pelo package `main`, ou algum outro local que
  nunca pode ser importado por outro módulo.
- `EFFECTIVELY_PRIVATE`: Embora a vulnerabilidade ocorra em um package Go que
  pode ser importado por outro módulo, o package não é destinado para uso
  externo e provavelmente nunca será importado fora do módulo em que está
  definido.
- `DEPENDENT_VULNERABILITY`: Esta vulnerabilidade é um subconjunto de outra
  vulnerabilidade no banco de dados. Por exemplo, se o package A contém uma
  vulnerabilidade, o package B depende do package A, e há IDs CVE separados
  para packages A e B, podemos marcar o relatório para B como uma vulnerabilidade
  dependente totalmente subsumida pelo relatório para A.
- `NOT_A_VULNERABILITY`: Embora um ID CVE ou GHSA tenha sido atribuído, não há
  vulnerabilidade conhecida associada a ele.
- `WITHDRAWN`: A vulnerabilidade foi retirada por sua fonte.

No momento, relatórios excluídos não são servidos via
API [vuln.go.dev](https://vuln.go.dev). No entanto, se você tem
um caso de uso específico e seria útil ter acesso a essas informações
através da API,
[por favor nos avise](/s/govulncheck-feedback).
