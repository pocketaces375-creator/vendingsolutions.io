#!/usr/bin/env python3
"""Bundle dist/ into ONE self-contained preview page (preview/index.html) for viewing on a phone:
all pages inline, switched by #hash, images inlined, chat widget left out. Run build.py first."""
import base64, glob, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
OUT = os.path.join(ROOT, "preview")


def key(path):
    return path.strip("/").replace("/", "-") or "home"


def data_uri(name):
    b = open(os.path.join(DIST, "assets", name), "rb").read()
    mime = "image/svg+xml" if name.endswith(".svg") else "image/webp"
    return f"data:{mime};base64,{base64.b64encode(b).decode()}"


pages = {}
header = footer = None
for f in sorted(glob.glob(f"{DIST}/**/index.html", recursive=True)):
    path = "/" + os.path.relpath(os.path.dirname(f), DIST).replace(".", "").strip("/")
    html = open(f).read()
    pages[key(path)] = re.search(r"<main>(.*)</main>", html, re.S).group(1)
    header = header or re.search(r'(<header class="top">.*?</header>)', html, re.S).group(1)
    footer = footer or re.search(r"(<footer>.*?</footer>)", html, re.S).group(1)

css = open(f"{DIST}/assets/style.css").read()
css = re.sub(r"url\(/assets/([\w.-]+)\)", lambda m: f"url({data_uri(m.group(1))})", css)


def relink(s):
    s = re.sub(r'class=on', '', s)
    return re.sub(r'href="(/[\w/-]*)"', lambda m: f'href="#{key(m.group(1))}"', s)


sections = "\n".join(f'<section class="pg" id="pg-{k}" hidden><main>{relink(v)}</main></section>' for k, v in pages.items())
doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vending Solutions website draft</title>
<style>{css}
.draftbar{{background:#ffb35c;color:#1a1020;text-align:center;font:600 13px system-ui;padding:6px}}</style></head><body>
<div class="draftbar">DRAFT preview of vendingsolutions.io (not live yet; live chat button appears on the real site)</div>
{relink(header)}
{sections}
{relink(footer)}
<script>
function show(){{var k=(location.hash||'#home').slice(1);var el=document.getElementById('pg-'+k)||document.getElementById('pg-home');
document.querySelectorAll('.pg').forEach(function(s){{s.hidden=s!==el}});
document.querySelectorAll('header nav a').forEach(function(a){{a.classList.toggle('on',a.getAttribute('href')==='#'+el.id.slice(3))}});
window.scrollTo(0,0)}}
window.addEventListener('hashchange',show);show();
document.querySelectorAll('form').forEach(function(f){{f.addEventListener('submit',function(e){{e.preventDefault();
f.insertAdjacentHTML('afterend','<p class="muted">Preview only: on the live site this sends your request to Vending Solutions.</p>')}})}});
</script></body></html>"""
os.makedirs(OUT, exist_ok=True)
open(f"{OUT}/index.html", "w").write(doc)
print(f"{OUT}/index.html", len(doc) // 1024, "KB,", len(pages), "pages:", ", ".join(pages))
