#!/usr/bin/env python3
"""Sobe o servidor do site e confere cada página traduzida: status HTTP, título e erros de template."""
import html
import json
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BIN, GOROOT = sys.argv[1], sys.argv[2]
ERRORS = re.compile(r"template: |error calling|executing \"|<no value>")


def free_port():
    with socket.socket() as s:
        s.bind(("localhost", 0))
        return s.getsockname()[1]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def get(url):
    try:
        with OPENER.open(url, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def meta(t, path):
    if path.endswith(".article"):
        return {"title": t.split("\n", 1)[0].strip()}
    if t.startswith("<!--{"):
        m = re.match(r"<!--(\{.*?\})-->", t, re.S)
        return {k.lower(): v for k, v in json.loads(m.group(1)).items()} if m else {}
    if t.startswith("---"):
        fm = t.split("---", 2)[1]
        out = {}
        for line in fm.splitlines():
            m = re.match(r"^(\w+):\s*(.*)$", line)
            if m:
                out[m.group(1).lower()] = m.group(2).strip().strip("'\"")
        return out
    return {}


def urls(path):
    rel = path[len("_content/"):]
    if rel.startswith("tour/"):
        return [f"/tour/lesson/{Path(rel).stem}"]
    page = re.sub(r"(index)?\.(md|html)$", "", rel)
    out = [f"/go.dev/{page}"]
    if rel.startswith("gopls/doc/"):
        out.append("/tip.golang.org/gopls/" + re.sub(r"(index)?\.md$", "", rel[len("gopls/doc/"):]))
    return out


def main():
    files = subprocess.run(["git", "grep", "-l", "ia-translated", "--", "_content"],
                           cwd=ROOT, capture_output=True, text=True).stdout.split()
    files = [f for f in files if f.endswith((".md", ".html", ".article"))]
    port = free_port()
    srv = subprocess.Popen([BIN, f"-http=localhost:{port}", "-content=_content", f"-goroot={GOROOT}"],
                           cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    base = f"http://localhost:{port}"
    try:
        for _ in range(120):
            if srv.poll() is not None:
                print("✗ o servidor não iniciou:\n" + srv.stdout.read()[-2000:])
                sys.exit(1)
            try:
                get(base + "/")
                break
            except OSError:
                time.sleep(0.5)
        bad = 0
        for f in files:
            m = meta((ROOT / f).read_text(), f)
            problems, status = [], None
            for u in urls(f):
                status, body = get(base + u)
                if status != 404:
                    break
            if "redirect" in m or m.get("link"):
                if status not in (200, 301, 302, 307, 308):
                    problems.append(f"status {status} em {u}")
            elif status != 200:
                problems.append(f"status {status} em {u}")
            else:
                if ERRORS.search(body):
                    problems.append("erro de template no HTML: " + ERRORS.search(body).group(0))
                title = m.get("title")
                if title and title not in body and html.escape(title) not in body and html.escape(title, quote=False) not in body:
                    problems.append(f"título {title!r} não aparece na página (metadados ignorados?)")
            if problems:
                bad += 1
                print(f"✗ {f}: " + "; ".join(problems))
        print(f"{len(files) - bad}/{len(files)} páginas traduzidas OK")
        sys.exit(1 if bad else 0)
    finally:
        srv.terminate()


if __name__ == "__main__":
    main()
