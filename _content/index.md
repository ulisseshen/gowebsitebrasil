---
ia-translated: true
title: A Linguagem de Programação Go
summary: Go é uma linguagem de programação de código aberto que torna simples construir sistemas seguros e escaláveis.
---

{{$canShare := not googleCN}}

<section class="Hero bluebg">
  <div class="Hero-gridContainer">
    <div class="Hero-blurb">
      <h1>Construa sistemas simples, seguros e escaláveis com Go</h1>
      <ul class="Hero-blurbList">
        <li>
          <svg width="12" height="10" viewBox="0 0 12 10" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10.8519 0.52594L3.89189 7.10404L1.14811 4.51081L0 5.59592L3.89189 9.27426L12 1.61105L10.8519 0.52594Z" fill="white" fill-opacity="0.87">
          </svg>
          Uma linguagem de programação de código aberto com suporte do Google
        </li>
        <li>
          <svg width="12" height="10" viewBox="0 0 12 10" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10.8519 0.52594L3.89189 7.10404L1.14811 4.51081L0 5.59592L3.89189 9.27426L12 1.61105L10.8519 0.52594Z" fill="white" fill-opacity="0.87">
          </svg>
          Fácil de aprender e excelente para equipes
        </li>
        <li>
          <svg width="12" height="10" viewBox="0 0 12 10" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10.8519 0.52594L3.89189 7.10404L1.14811 4.51081L0 5.59592L3.89189 9.27426L12 1.61105L10.8519 0.52594Z" fill="white" fill-opacity="0.87">
          </svg>
          Concorrência integrada e uma biblioteca padrão robusta
        </li>
        <li>
          <svg width="12" height="10" viewBox="0 0 12 10" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10.8519 0.52594L3.89189 7.10404L1.14811 4.51081L0 5.59592L3.89189 9.27426L12 1.61105L10.8519 0.52594Z" fill="white" fill-opacity="0.87">
          </svg>
          Grande ecossistema de parceiros, comunidades e ferramentas
        </li>
      </ul>
    </div>
    <div class="Hero-actions">
      <div
        data-version=""
        class="js-latestGoVersion">
        <a class="Primary" href="/learn/" aria-label="Get Started" aria-describedby="getStarted-description" role="button">Get Started</a>
        <a class="Secondary js-downloadBtn" href="/dl" aria-label="Download" aria-describedby="download-description" role="button">Download</a>
        <div class="screen-reader-only" id="getStarted-description" hidden>
          Abre uma nova janela com o guia Get Started.
        </div>
        <div class="screen-reader-only" id="download-description" hidden>
          Abre uma nova janela para baixar o Go.
        </div>
      </div>
      <div class="Hero-footnote">
        <p>
          Baixe os pacotes para
          <a class="js-downloadWin">Windows 64-bit</a>,
          <a class="js-downloadMac">macOS</a>,
          <a class="js-downloadLinux">Linux</a>, e
          <a href="/dl/" aria-describedby="newwindow-description">mais</a>
        </p>
        <p>
          O comando <code>go</code> por padrão baixa e autentica
          módulos usando o Go module mirror e o Go checksum database mantidos pelo
          Google. <a href="/dl" aria-describedby="newwindow-description">Saiba mais.</a>
        </p>
      </div>
    </div>
    <div class="screen-reader-only" id="newwindow-description" hidden>
          Abre em nova janela.
    </div>
    <div class="Hero-gopher">
      <img class="Hero-gopherLadder" src="/images/gophers/ladder.svg" alt="Go Gopher subindo uma escada.">
    </div>
  </div>
</section>
<section class="WhoUses">
  <div class="WhoUses-gridContainer">
    <div class="WhoUses-header">
      <h2 class="WhoUses-headerH2">Empresas que usam Go</h2>
      <p class="WhoUses-subheader">Organizações de todos os setores usam Go para alimentar seus softwares e serviços
        <a href="/solutions/" class="WhoUsesCaseStudyList-seeAll" aria-describedby="newwindow-description">
        Ver todas as histórias
       </a>
     </p>
    </div>
  <div class="WhoUsesCaseStudyList">
    <ul class="WhoUsesCaseStudyList-gridContainer">
    {{- range newest (pages "/solutions/*")}}{{if eq .series "Case Studies"}}
      {{- if .link }}
        {{- if .inLandingPageGrid }}
          <li class="WhoUsesCaseStudyList-caseStudy">
            <a href="{{.link}}" aria-label="View CaseStudy of {{.company}}, (opens in new window)" target="_blank" rel="noopener"
              class="WhoUsesCaseStudyList-caseStudyLink">
              <img
                loading="lazy"
                height="48"
                width="30%"
                src="/images/logos/{{.logoSrc}}"
                class="WhoUsesCaseStudyList-logo"
                alt="">
            </a>
          </li>
        {{- end}}
      {{- else}}
        <li class="WhoUsesCaseStudyList-caseStudy">
          <a href="{{.URL}}" aria-label="View CaseStudy of {{.company}}, (opens in new window)" class="WhoUsesCaseStudyList-caseStudyLink">
            <img
              loading="lazy"
              height="48"
              width="30%"
              src="/images/logos/{{.logoSrc}}"
              class="WhoUsesCaseStudyList-logo"
              alt="">
            <p>Ver estudo de caso</p>
          </a>
        </li>
      {{- end}}
    {{- end}}
    {{- end}}
    </ul>
  </div>
</section>
<section class="TestimonialsGo">
  <div class="GoCarousel">
    <div class="GoCarousel-controlsContainer">
      <div class="GoCarousel-wrapper">
        <ul class="js-testimonialsGoQuotes TestimonialsGo-quotes">
          {{- range $index, $element := data "/testimonials.yaml"}}
            <li class="TestimonialsGo-quoteGroup GoCarousel-slide" id="quote_slide{{$index}}">
              <div class="TestimonialsGo-quoteSingleItem">
                <div class="TestimonialsGo-quoteSection">
                  <p class="TestimonialsGo-quote">{{raw .quote}}</p>
                  <div class="TestimonialsGo-author">— {{.name}},
                    <span class="NoWrapSpan">{{.title}}</span>
                    <span class="NoWrapSpan"> at {{.company}}</span>
                  </div>
                </div>
              </div>
            </li>
          {{- end}}
        </ul>
      </div>
    <button class="js-testimonialsPrev GoCarousel-controlPrev" hidden>
      <i class="GoCarousel-icon material-icons">navigate_before</i>
    </button>
    <button class="js-testimonialsNext GoCarousel-controlNext">
      <i class="GoCarousel-icon material-icons">navigate_next</i>
    </button>
  </div>
  </div>
</section>
<section class="Playground">
  <div class="Playground-gridContainer">
    <div class="Playground-headerContainer">
      <h2 class="HomeSection-header">Experimente Go</h2>
    </div>
    <div class="Playground-inputContainer">
      <div class="Playground-preContainer">
        Pressione Esc para sair do editor.
      </div>
      <textarea class="Playground-input js-playgroundCodeEl" spellcheck="false" aria-label="Try Go" aria-describedby="editor-description" id="code">
// You can edit this code!
// Click here and start typing.
package main
import "fmt"
func main() {
  fmt.Println("Hello, 世界")
}</textarea>
    </div>
    <div class="screen-reader-only" id="editor-description" hidden>
      Pressione Esc para sair do editor.
    </div>
    <div class="Playground-outputContainer js-playgroundOutputEl">
      <pre class="Playground-output"><noscript>Hello, 世界</noscript></pre>
    </div>
    <div class="Playground-controls">
      <select class="Playground-selectExample js-playgroundToysEl" aria-label="Code examples">
      <option value="hello.go">Hello, World!</option>
      <option value="life.go">Conway's Game of Life</option>
      <option value="fib.go">Fibonacci Closure</option>
      <option value="peano.go">Peano Integers</option>
      <option value="pi.go">Concurrent pi</option>
      <option value="sieve.go">Concurrent Prime Sieve</option>
      <option value="solitaire.go">Peg Solitaire Solver</option>
      <option value="tree.go">Tree Comparison</option>
      </select>
      <div class="Playground-buttons">
      <button class="Button Button--primary js-playgroundRunEl Playground-runButton" title="Run this code [shift-enter]">Run</button>
      <div class="Playground-secondaryButtons">
        {{- if $canShare}}
        <button class="Button js-playgroundShareEl Playground-button" title="Share in Go Playground">Share</button>
        {{- end}}
        <a class="Button tour Playground-button" href="/tour/" title="Tour Go from your browser">Tour</a>
      </div>
      </div>
    </div>
  </div>
</section>
<section class="WhyGo">
  <div class="WhyGo-gridContainer">
    <div class="WhyGo-header">
      <h2 class="WhyGo-headerH2">O que é possível com Go</h2>
      <p class="WhyGo-subheader">
        Use Go para uma variedade de propósitos de desenvolvimento de software
      </p>
    </div>
    <ul class="WhyGo-reasons">
      {{- range first 4 (data "/resources.yaml")}}
        <li class="WhyGo-reason">
          <div class="WhyGo-reasonDetails">
            <div class="WhyGo-reasonIcon" role="presentation">
              <img class="DarkMode-img" src="{{.iconDark}}" alt="{{.iconName}}">
              <img class="LightMode-img" src="{{.icon}}" alt="{{.iconName}}">
            </div>
            <div class="WhyGo-reasonText">
              <h3 class="WhyGo-reasonTitle">{{.title}}</h3>
              <p>
                {{.description}}
              </p>
            </div>
          </div>
          <div class="WhyGo-reasonFooter">
            <div class="WhyGo-reasonPackages">
              <div class="WhyGo-reasonPackagesHeader">
                <img src="/images/icons/package.svg" alt="Packages.">
                Packages Populares:
              </div>
              <ul class="WhyGo-reasonPackagesList">
                {{- range .packages }}
                  <li class="WhyGo-reasonPackage">
                    <a class="WhyGo-reasonLink" href="{{.url}}" target="_blank" rel="noopener">
                      {{.title}}
                    </a>
                  </li>
                  {{- end}}
              </ul>
            </div>
            <div class="WhyGo-reasonLearnMoreLink">
              <a href="{{.link}}" aria-describedby="newwindow-description">Saiba Mais
              <i class="material-icons WhyGo-forwardArrowIcon" aria-hidden="true">arrow_forward</i></a>
            </div>
          </div>
        </li>
      {{- end}}
      {{- if gt (len (data "resources.yaml")) 3}}
        <li class="WhyGo-reason">
          <div class="WhyGo-reasonShowMore">
            <div class="WhyGo-reasonShowMoreImgWrapper">
              <img
                class="WhyGo-reasonShowMoreImg"
                loading="lazy"
                height="148"
                width="229"
                src="/images/gophers/biplane.svg"
                alt="Go Gopher andando de skate.">
            </div>
            <div class="WhyGo-reasonShowMoreLink">
              <a href="/solutions/use-cases" aria-describedby="newwindow-description">Mais casos de uso
              <i class="material-icons
              WhyGo-forwardArrowIcon" aria-hidden="true">arrow_forward</i></a>
            </div>
          </div>
        </li>
      {{- end}}
    </ul>
  </div>
</section>
<section class="GettingStartedGo">
  <div class="GettingStartedGo-gridContainer">
    <div class="GettingStartedGo-header">
      <h2 class="GettingStartedGo-headerH2">Começando com Go</h2>
      <p class="GettingStartedGo-headerDesc">
        Explore uma riqueza de recursos de aprendizado, incluindo jornadas guiadas, cursos, livros e muito mais.
      </p>
      <div class="GettingStartedGo-ctas">
        <a class="GettingStartedGo-primaryCta" href="/learn/"aria-describedby="newwindow-description">Get Started</a>
        <a href="/doc/install/" aria-describedby="newwindow-description">Download Go</a>
      </div>
    </div>
    <div class="GettingStartedGo-resourcesSection">
      <ul class="GettingStartedGo-resourcesList">
        <li class="GettingStartedGo-resourcesHeader">
          Recursos para começar por conta própria
        </li>
        <li class="GettingStartedGo-resourceItem">
          <a href="/learn#guided-learning-journeys" class="GettingStartedGo-resourceItemTitle" aria-describedby="newwindow-description">
            Jornadas de aprendizado guiadas
          </a>
          <div class="GettingStartedGo-resourceItemDescription">
            Tutoriais passo a passo para dar seus primeiros passos
          </div>
        </li>
        <li class="GettingStartedGo-resourceItem">
          <a href="/learn#online-learning" class="GettingStartedGo-resourceItemTitle" aria-describedby="newwindow-description">
            Aprendizado online
          </a>
          <div class="GettingStartedGo-resourceItemDescription">
            Navegue pelos recursos e aprenda no seu próprio ritmo
          </div>
        </li>
        <li class="GettingStartedGo-resourceItem">
          <a href="/learn#featured-books" class="GettingStartedGo-resourceItemTitle" aria-describedby="newwindow-description">
            Livros em destaque
          </a>
          <div class="GettingStartedGo-resourceItemDescription">
            Leia capítulos estruturados e teorias
          </div>
        </li>
        <li class="GettingStartedGo-resourceItem">
          <a href="/learn#self-paced-labs" class="GettingStartedGo-resourceItemTitle" aria-describedby="newwindow-description">
            Cloud Self-paced labs
          </a>
          <div class="GettingStartedGo-resourceItemDescription">
            Mergulhe no deploy de apps Go no GCP
          </div>
        </li>
      </ul>
      <ul class="GettingStartedGo-resourcesList">
        <li class="GettingStartedGo-resourcesHeader">
          Treinamentos Presenciais
        </li>
        {{- range first 4 (data "/learn/training.yaml")}}
          <li class="GettingStartedGo-resourceItem">
            <a href="{{.url}}" class="GettingStartedGo-resourceItemTitle" aria-describedby="newwindow-description">
              {{.title}}
            </a>
            <div class="GettingStartedGo-resourceItemDescription">
              {{.blurb}}
            </div>
          </li>
        {{- end}}
      </ul>
    </div>
  </div>
</section>
<script src="/js/index.js" defer></script>
