# Plano de Tradução 04: Tour, Learn e Solutions

> **Agente de Tradução:** Use o agente `.claude/agents/tradutor.md` para todas as traduções
>
> **Prioridade:** ALTA - Conteúdo interativo e casos de uso

## Instruções de Uso

Para traduzir qualquer arquivo deste plano, execute:
```
@tradutor Traduza o arquivo [caminho-do-arquivo]
```

Após traduzir cada arquivo, marque o checkpoint com `[x]`.

---

## Seção 1: Tour of Go (Artigos Principais)

> **NOTA:** Os arquivos `.article` contêm o texto do tour. Os arquivos `.go` são exemplos de código que NÃO devem ser traduzidos.

### 1.1 Artigos do Tour
- [x] `_content/tour/welcome.article` - Boas-vindas
- [x] `_content/tour/basics.article` - Básicos
- [x] `_content/tour/flowcontrol.article` - Controle de fluxo
- [x] `_content/tour/moretypes.article` - Mais tipos
- [x] `_content/tour/methods.article` - Métodos
- [x] `_content/tour/concurrency.article` - Concorrência
- [x] `_content/tour/generics.article` - Generics

### 1.2 Templates e Partials (Opcional)

> Traduzir apenas textos de UI visíveis ao usuário

- [ ] `_content/tour/static/partials/format-tab.html`
- [ ] `_content/tour/static/partials/nav.html`
- [ ] `_content/tour/static/partials/run-tab.html`
- [ ] `_content/tour/static/partials/toc.html`
- [ ] `_content/tour/static/partials/toc-code.html`

---

## Seção 2: Learn (Recursos de Aprendizado)

### 2.1 Página Principal
- [x] `_content/learn/index.md` - Página principal Learn

### 2.2 Arquivos YAML (Descrições de Recursos)

> Traduzir títulos e descrições dentro dos YAMLs

- [x] `_content/learn/books.yaml` - Livros recomendados
- [x] `_content/learn/courses.yaml` - Cursos online
- [x] `_content/learn/guided.yaml` - Guias de aprendizado
- [x] `_content/learn/quickstart.yaml` - Início rápido
- [x] `_content/learn/training.yaml` - Treinamentos
- [x] `_content/learn/tutorials.yaml` - Tutoriais
- [x] `_content/learn/cloud.yaml` - Cloud

---

## Seção 3: Solutions (Casos de Uso)

### 3.1 Páginas Principais
- [ ] `_content/solutions/index.md` - Índice de solutions
- [ ] `_content/solutions/case-studies.md` - Casos de estudo
- [ ] `_content/solutions/use-cases.md` - Casos de uso

### 3.2 Casos de Uso por Categoria
- [ ] `_content/solutions/cloud.md` - Cloud
- [ ] `_content/solutions/clis.md` - CLIs
- [ ] `_content/solutions/devops.md` - DevOps
- [ ] `_content/solutions/webdev.md` - Web Development

### 3.3 Estudos de Caso - Empresas (A-C)
- [ ] `_content/solutions/allegro.md` - Allegro
- [ ] `_content/solutions/americanexpress.md` - American Express
- [ ] `_content/solutions/armut.md` - Armut
- [ ] `_content/solutions/bitly.md` - Bitly
- [ ] `_content/solutions/bytedance.md` - ByteDance
- [ ] `_content/solutions/capital-one.md` - Capital One
- [ ] `_content/solutions/chrome.md` - Chrome
- [ ] `_content/solutions/cloudflare.md` - Cloudflare
- [ ] `_content/solutions/cockroachlabs.md` - CockroachLabs
- [ ] `_content/solutions/coredata.md` - CoreData
- [ ] `_content/solutions/curve.md` - Curve

### 3.4 Estudos de Caso - Empresas (D-M)
- [ ] `_content/solutions/dropbox.md` - Dropbox
- [ ] `_content/solutions/facebook.md` - Facebook
- [ ] `_content/solutions/firebase.md` - Firebase
- [ ] `_content/solutions/grail.md` - Grail
- [x] `_content/solutions/mercadolibre.md` - MercadoLibre
- [ ] `_content/solutions/microsoft.md` - Microsoft
- [ ] `_content/solutions/monzo.md` - Monzo

### 3.5 Estudos de Caso - Empresas (N-Z)
- [x] `_content/solutions/netflix.md` - Netflix
- [ ] `_content/solutions/paypal.md` - PayPal
- [ ] `_content/solutions/riotgames.md` - Riot Games
- [ ] `_content/solutions/salesforce.md` - Salesforce
- [ ] `_content/solutions/sitereliability.md` - Site Reliability
- [ ] `_content/solutions/sixt.md` - Sixt
- [ ] `_content/solutions/stream.md` - Stream
- [ ] `_content/solutions/trivago.md` - Trivago
- [ ] `_content/solutions/twitch.md` - Twitch
- [x] `_content/solutions/uber.md` - Uber
- [ ] `_content/solutions/wildlifestudios.md` - Wildlife Studios
- [ ] `_content/solutions/x.md` - X (Twitter)

### 3.6 Google Solutions
- [ ] `_content/solutions/google/index.md` - Google Index
- [ ] `_content/solutions/google/chrome.md` - Google Chrome
- [ ] `_content/solutions/google/coredata.md` - Google Core Data
- [ ] `_content/solutions/google/firebase.md` - Google Firebase
- [ ] `_content/solutions/google/sitereliability.md` - Google SRE

---

## Seção 4: Páginas Root (_content/)

- [ ] `_content/index.md` - Página inicial
- [ ] `_content/about.md` - Sobre
- [ ] `_content/brand.md` - Marca Go
- [ ] `_content/conduct.html` - Código de conduta
- [ ] `_content/help.md` - Ajuda
- [ ] `_content/project.html` - Projeto
- [ ] `_content/security.md` - Segurança

---

## Seção 5: gopls Documentation

- [ ] `_content/gopls/doc/index.md` - Gopls Index
- [ ] `_content/gopls/doc/settings.md` - Gopls Settings

---

## Seção 6: Reference (ref/)

- [ ] `_content/ref/mod.md` - Module Reference (arquivo grande ~219KB)

---

## Seção 7: Wiki

- [ ] `_content/wiki/Comments.md` - Comentários Wiki

---

## Progresso

| Seção | Total | Traduzidos | Progresso |
|-------|-------|------------|-----------|
| Tour Articles | 7 | 7 | 100% |
| Tour Templates | 5 | 0 | 0% |
| Learn | 8 | 8 | 100% |
| Solutions Principal | 7 | 0 | 0% |
| Solutions A-C | 11 | 0 | 0% |
| Solutions D-M | 7 | 1 | 14% |
| Solutions N-Z | 12 | 2 | 17% |
| Google Solutions | 5 | 0 | 0% |
| Root Pages | 7 | 0 | 0% |
| gopls | 2 | 0 | 0% |
| ref | 1 | 0 | 0% |
| Wiki | 1 | 0 | 0% |
| **TOTAL** | **73** | **18** | **25%** |

---

## Notas Importantes

### Tour of Go
- Os arquivos `.article` usam um formato especial - mantenha a estrutura
- NÃO traduza código nos arquivos `.go` - eles são exemplos executáveis
- Traduza apenas comentários e textos explicativos

### Learn
- YAMLs contêm referências a recursos externos
- Mantenha URLs originais
- Traduza apenas títulos e descrições

### Solutions
- Casos de estudo são importantes para convencer empresas brasileiras
- Mantenha nomes de empresas em inglês
- Traduza métricas e resultados

### ref/mod.md
- Arquivo muito grande (~219KB)
- Considere traduzir em sessões
- Alta prioridade por ser documentação de referência
