#!/usr/bin/env python3
"""Compara cada arquivo traduzido (marcado com ia-translated) com a versão do upstream."""
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REF = sys.argv[1] if len(sys.argv) > 1 else "upstream/master"
FENCE = re.compile(r"^```.*?^```", re.S | re.M)


def upstream(path):
    r = subprocess.run(["git", "show", f"{REF}:{path}"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def strip_fences(t):
    return FENCE.sub("", t)


def anchors(t):
    t = strip_fences(t)
    return Counter(re.findall(r"\{#[^}\s]+\}", t) + re.findall(r'\bid="[^"]+"', t))


def has_template_flag(t):
    head = t[:600]
    return bool(re.search(r'^template:\s*true\s*$', head, re.M | re.I) or re.search(r'"template":\s*true', head, re.I))


def check_article(path, t, up, errs):
    first_block = t.split("\n\n", 1)[0].split("\n")
    if any("ia-translated" in l for l in first_block):
        errs.append("marcador ia-translated dentro do cabeçalho; coloque-o depois do bloco de autor")
    elif up is not None and len(first_block) != len(up.split("\n\n", 1)[0].split("\n")):
        errs.append("cabeçalho (título/subtítulo) com número de linhas diferente do upstream")
    if up is not None:
        for d in (".play", ".code", ".image", ".iframe", ".html"):
            n_up = len(re.findall(rf"^{re.escape(d)} ", up, re.M))
            n = len(re.findall(rf"^{re.escape(d)} ", t, re.M))
            if n != n_up:
                errs.append(f"diretivas {d}: {n} (upstream {n_up})")
        slides_up, slides = len(re.findall(r"^\* ", up, re.M)), len(re.findall(r"^\* ", t, re.M))
        if slides != slides_up:
            errs.append(f"slides '* ': {slides} (upstream {slides_up})")


def check(path):
    t = (ROOT / path).read_text()
    up = upstream(path)
    errs = []

    if path.endswith(".article"):
        check_article(path, t, up, errs)
    if up is not None:
        if up.startswith("<!--{") and not t.startswith("<!--{"):
            errs.append("o arquivo precisa começar com o cabeçalho <!--{ ... }--> como no upstream")
        if up.startswith("---") and not t.startswith("---"):
            errs.append("o arquivo precisa começar com o frontmatter --- como no upstream")
        if has_template_flag(up) != has_template_flag(t):
            errs.append("flag template: true / \"Template\": true diferente do upstream")
        cu, ct = FENCE.findall(up), FENCE.findall(t)
        if cu != ct:
            diff = sum(a != b for a, b in zip(cu, ct)) + abs(len(cu) - len(ct))
            errs.append(f"blocos de código diferentes do upstream ({diff} de {len(cu)}); código não deve ser traduzido")
        au, at = anchors(up), anchors(t)
        if au != at:
            miss, extra = list((au - at).elements())[:5], list((at - au).elements())[:5]
            errs.append(f"âncoras/IDs diferentes do upstream: faltam {miss} sobram {extra}")
    if t.startswith("<!--{"):
        m = re.match(r"<!--(\{.*?\})-->", t, re.S)
        try:
            json.loads(m.group(1) if m else "")
        except ValueError:
            errs.append("cabeçalho <!--{ }--> não é JSON válido")

    defined = {a[2:-1] for a in re.findall(r"\{#[^}\s]+\}", t)} | set(re.findall(r'\bid="([^"]+)"', t))
    if path.endswith((".md", ".html")) and defined:
        body = strip_fences(t)
        targets = set(re.findall(r"\]\(#([^)\s]+)\)", body)) | set(re.findall(r'href="#([^"]+)"', body))
        broken = sorted(targets - defined)
        if broken:
            errs.append(f"links internos sem âncora: {broken[:5]}")
    return errs


def main():
    files = subprocess.run(
        ["git", "grep", "-l", "-E", "ia-translated|_ia_translated", "--", "_content"],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.split()
    files = [f for f in files if not f.endswith(".go")]
    bad = 0
    for f in files:
        errs = check(f)
        if errs:
            bad += 1
            print(f"✗ {f}")
            for e in errs:
                print(f"    - {e}")
    print(f"{len(files) - bad}/{len(files)} arquivos traduzidos OK")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
