---
ia-translated: true
title: O Blog Go
---

<div id="blogindex">

{{range first 10 (newest (pages "/blog/*.md")) -}}
{{if .date}}
<p class="blogtitle">
  <a href="{{.URL}}" aria-describedby="blog-description">{{.title}}</a>, <span class="date">{{.date.Format "2 January 2006"}}</span><br>
  <span class="author">{{with .by}}{{by .}}<br>{{end}}</span>
  {{with .Tags}}<span class="tags">{{range .}}{{.}} {{end}}</span>{{end}}
</p>
<p class="blogsummary">
  {{.summary}}
</p>
{{end}}
{{end}}

<p class="blogtitle">
<a href="/blog/all" aria-label="Mais artigos" aria-describedby="blog-description">Mais artigos...</a>
</p>

<div class="screen-reader-only" id="blog-description" hidden>
    Abre em nova janela.
</div>
