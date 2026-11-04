#!/usr/bin/env python3
"""Build vendingsolutions.io as a static site (no hosting bill, no WordPress).

  python3 build.py          -> dist/  (upload dist/ to any static host: GitHub Pages, Cloudflare Pages, ...)

Edit site.json for phone numbers, socials and LOCATIONS. Each location becomes its own page
(/locations/<slug>/) with LocalBusiness data and a link to its Google reviews, which is what
local search ranks on. Old WordPress URLs (/services/, /find-our-machines/, /schedule-free-consult/)
are kept so existing links and rankings carry over. Content recovered from the Apr 2026 site."""
import html, json, os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(ROOT, "site.json")))
OUT = os.path.join(ROOT, "dist")
E = html.escape


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def tel(p):
    return "+1" + re.sub(r"\D", "", p)


NAV = [("/", "Home"), ("/services/", "Our Services"), ("/find-our-machines/", "Find Our Machines"),
       ("/partners/", "Partner With Us")]


def page(path, title, desc, body, schema=None):
    nav = "".join(f'<a href="{h}"{" class=on" if h == path else ""}>{t}</a>' for h, t in NAV)
    phones = " · ".join(f'<a href="tel:{tel(p)}">{p}</a>' for p in S["phones"])
    social = " ".join(f'<a href="{u}" rel="me">{n.title()}</a>' for n, u in S["social"].items() if u)
    ld = json.dumps(schema or org_schema(), ensure_ascii=False)
    chat = f'<script src="{S["chat_widget"]}" defer></script>' if S.get("chat_widget") else ""
    doc = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{S['url']}{path}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website"><meta property="og:url" content="{S['url']}{path}">
<meta property="og:image" content="{S['url']}/assets/hero-vapor.webp">
<link rel="icon" href="/assets/favicon.svg">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{ld}</script>
</head><body>
<header class="top"><a class="brand" href="/"><span class="mark">VS</span> {E(S['name'])}</a>
<nav>{nav}</nav><a class="btn small" href="/schedule-free-consult/">Free Consultation</a></header>
<main>{body}</main>
<footer><div class="cols"><div><b>{E(S['name'])}</b><br>Smart vape vending for bars, venues and businesses across {E(S['area'])}.<br>
<span class="muted">Sale of nicotine products to anyone under 21 is prohibited by Florida law. Proof of age required.</span></div>
<div><b>Contact</b><br>{phones}<br><a href="mailto:{S['email']}">{S['email']}</a></div>
<div><b>Pages</b><br>{'<br>'.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}<br><a href="/schedule-free-consult/">Free Consultation</a></div></div>
<p class="muted">© 2026 {E(S['name'])} · {E(S['legal'])}. All rights reserved. {social}</p></footer>
{chat}
</body></html>"""
    d = os.path.join(OUT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(doc)


def org_schema():
    return {"@context": "https://schema.org", "@type": "LocalBusiness", "name": S["name"], "url": S["url"],
            "telephone": tel(S["phones"][0]), "email": S["email"], "areaServed": S["area"],
            "address": {"@type": "PostalAddress", "addressRegion": S["region"], "addressCountry": "US"},
            "description": "Free smart vape vending machines for bars, venues and businesses: installed, stocked and serviced at no cost."}


def cta(text="Order a FREE machine and installation"):
    return f'<section class="cta"><h2>{text}</h2><p>No cost, no stock to hold, no hassle. We handle permits, installation, restocking and support.</p><a class="btn" href="/schedule-free-consult/">Order FREE Now</a></section>'


FEATURES = ["Greatly increased customer retention", "Small footprint: 30 in × 30 in, wall mounted", "Risk-free revenue",
            "Digital touchscreen with an intuitive interface", "Zero cost to you", "Designed to fit any location",
            "Fully managed and serviced", "Digital advertising space for extra revenue", "Built-in age verification"]
STEPS = [("Contact us", "Call, chat or book a free consultation."), ("Order your free unit", "We size and design the machine for your venue."),
         ("Free installation", "We handle permits and install it."), ("Auto replenish", "The machine reports its stock every minute, and we restock automatically."),
         ("Get paid", "You earn revenue with no upfront cost."), ("24/7 customer service", "Our support line answers your customers any time, day or night.")]
FAQ = [("Is this legal at my site?", "Yes. The machines and products comply with all applicable laws, and we take care of all permits at no cost to you. We're fully DBPR compliant."),
       ("How do you prevent underage purchases?", "We take it very seriously. In venues that don't check ID at the door, the machine's built-in age verification is always active. The sale of nicotine products to anyone under 21 is against Florida law."),
       ("What if vaping isn't allowed inside my venue?", "Many of our partners don't allow vaping indoors. Customers buy inside to use outside (and for the next couple of days), and they don't leave early to find a store."),
       ("Does this promote vaping at my site?", "No. It adds convenience for adults who already vape (about 1 in 7 people), which makes your venue more appealing."),
       ("Do I have to fill the machine or hold stock?", "No. A zero-cost service agreement is included. The machine's telemetry reports stock levels every minute, which triggers automatic restocking."),
       ("Which vapes do you stock?", "We tailor the selection to your clientele, and we're happy to stock what your customers ask for."),
       ("What if something goes wrong with a purchase?", "Customers can reach our support line 24/7. Most issues, including refunds, are resolved on the spot.")]


def build():
    shutil.rmtree(OUT, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    feats = "".join(f"<li>{f}</li>" for f in FEATURES)
    steps = "".join(f'<div class="step"><span>Step {i:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(STEPS, 1))
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

    page("/", f"{S['name']} | Free Smart Vape Vending Machines in {S['area']}",
         "Add a new revenue stream at zero cost. Free smart vape vending machines for bars and venues across South Florida: installed, stocked and serviced for free, with 24/7 customer support.",
         f"""<section class="hero"><div class="in"><p class="kicker">Smart vape vending · {E(S['area'])}</p>
<h1>Take advantage of a new revenue stream for <em>zero cost</em></h1>
<p class="lead">We install, stock and service a smart vending machine at your location for free. You earn. Your customers stay longer.</p>
<div class="row"><a class="btn" href="/schedule-free-consult/">Order FREE Now</a><a class="btn ghost" href="tel:{tel(S['phones'][0])}">Call {S['phones'][0]}</a></div></div></section>
<section class="cards3">
<div class="card"><h3>Full installation and maintenance</h3><p>We size and design the machine for your business, install it, and service it for free.</p><a href="/services/">Learn more →</a></div>
<div class="card"><h3>Advanced vending machine</h3><p>A smart machine with products that keep customers at your location longer and bring new ones in.</p><a href="/services/">Learn more →</a></div>
<div class="card"><h3>Real-time advertising</h3><p>The touchscreen plays your videos and pictures to promote events, menu items and more.</p><a href="/services/">Learn more →</a></div></section>
<section class="split"><div><h2>South Florida's smart vape vending partner</h2><ul class="ticks">{feats}</ul></div>
<div class="panel"><h3>Always on</h3><p>Every machine reports its stock every minute, restocks automatically, and is backed by a 24/7 customer support line.</p></div></section>
<section><h2 class="c">How it works</h2><div class="steps">{steps}</div></section>
<section class="faq"><h2 class="c">Frequently asked questions</h2>{faq}</section>
{cta()}""", schema=[org_schema(), faq_ld])

    page("/services/", f"Services | {S['name']}",
         "Free installation, full maintenance, smart vending machines with age verification, and touchscreen advertising for your venue.",
         """<section class="head"><h1>Vending solutions tailored to your venue</h1><p class="lead">State-of-the-art vending that adds convenience for your customers and revenue for you, with nothing to manage.</p></section>
<section class="cards3">
<div class="card"><h3>Full installation and maintenance</h3><p>All repairs, cleaning and upkeep are included, and emergency service is available around the clock to keep downtime near zero. We also handle the permits.</p></div>
<div class="card"><h3>Advanced vending machine</h3><p>A compact, wall-mounted smart machine (30 in × 30 in) with a touchscreen, card payments and built-in age verification. Stock levels are reported every minute, so it's never empty.</p></div>
<div class="card"><h3>Real-time advertising</h3><p>Use the screen to promote your specials, events and menu, or earn extra from digital ad space.</p></div></section>
<section class="split"><div><h2>24/7 customer support</h2><p>Every machine is backed by our support line and live chat. Customers get help immediately, including refunds for a failed purchase, so your staff never has to deal with it.</p></div>
<div class="panel"><h3>Zero cost, zero risk</h3><p>No equipment cost, no stock to buy, no staff time. You get a share of the revenue.</p></div></section>""" + cta())

    locs = S.get("locations") or []
    loc_html = "".join(
        f'<a class="loc" href="/locations/{slug(l["name"])}/"><b>{E(l["name"])}</b><span>{E(l.get("city", ""))}</span>'
        f'{"<em>★ " + str(l["rating"]) + "</em>" if l.get("rating") else ""}</a>' for l in locs)
    page("/find-our-machines/", f"Find Our Machines | {S['name']}",
         "Find a Vending Solutions machine near you in South Florida, or contact us for the nearest location.",
         f"""<section class="head"><h1>Find our machines</h1><p class="lead">Looking for the nearest machine? Call, chat or email us and we'll point you to it.</p>
<p class="contact">{" · ".join(f'<a href="tel:{tel(p)}">{p}</a>' for p in S['phones'])} · <a href="mailto:{S['email']}">{S['email']}</a></p></section>
{f'<section><div class="locs">{loc_html}</div></section>' if locs else ''}
<section class="split"><div><h2>Want a machine at your location?</h2><p>We offer free installation and maintenance. We handle everything from setup to restocking, so it's hassle-free for you and your customers.</p></div></section>""" + cta())

    for l in locs:   # one page per location: what local search and review links rank on
        ls = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": f"{S['name']} at {l['name']}",
              "url": f"{S['url']}/locations/{slug(l['name'])}/", "telephone": tel(S["phones"][0]),
              "address": {"@type": "PostalAddress", "streetAddress": l.get("address", ""), "addressLocality": l.get("city", ""),
                          "addressRegion": S["region"], "addressCountry": "US"}}
        if l.get("rating") and l.get("review_count"):
            ls["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": l["rating"], "reviewCount": l["review_count"]}
        page(f"/locations/{slug(l['name'])}/", f"Vape vending at {l['name']}, {l.get('city', '')} | {S['name']}",
             f"Smart vape vending machine at {l['name']} in {l.get('city', '')}. 21+ with ID. 24/7 support.",
             f"""<section class="head"><h1>{E(l['name'])}</h1><p class="lead">{E(l.get('address', ''))} {E(l.get('city', ''))}</p>
{f'<p><a class="btn" href="{l["reviews_url"]}">See reviews on Google</a></p>' if l.get('reviews_url') else ''}
{f'<p><a class="btn ghost" href="{l["maps_url"]}">Directions</a></p>' if l.get('maps_url') else ''}</section>""", schema=ls)

    page("/partners/", f"Partner With Us | {S['name']}",
         "Partner with Vending Solutions: 24/7 AI customer service, live machine monitoring, automatic restocking and monthly reporting for vending operators and venues.",
         """<section class="head"><h1>Partner with us</h1><p class="lead">Our infrastructure is our edge. Plug your machines or venues into the same system that runs ours.</p></section>
<section class="cards3">
<div class="card"><h3>24/7 customer service</h3><p>A support line and live chat that never sleep. Every call becomes a ticket, refunds are handled on the spot, and owners get a daily summary.</p></div>
<div class="card"><h3>Live machine monitoring</h3><p>Stock, sales and machine health in real time, with alerts before a machine goes empty or offline.</p></div>
<div class="card"><h3>Reporting you can trust</h3><p>Monthly reports covering sales, refunds, support calls and response times, per machine and per location.</p></div></section>""" + cta("Let's talk partnership"))

    page("/schedule-free-consult/", f"Schedule a Free Consultation | {S['name']}",
         "Book a free consultation to get a smart vape vending machine installed at your venue at no cost.",
         f"""<section class="head"><h1>Schedule your free consultation</h1><p class="lead">Tell us about your venue. We'll learn your goals and recommend the right setup, at no cost and with no obligation.</p></section>
<section class="formwrap"><form id="consult" class="form">
<label>What do you need?<select name="kind"><option value="placement">A free machine for my venue</option><option value="callback">Please call me back</option><option value="question">I have a question</option></select></label>
<label>Name<input name="name" required autocomplete="name"></label>
<label>Venue / business name<input name="business" autocomplete="organization"></label>
<label>City<input name="city" autocomplete="address-level2"></label>
<label>Phone number<input name="phone" type="tel" autocomplete="tel"></label>
<label>Email<input name="email" type="email" autocomplete="email"></label>
<label>Message<textarea name="message" rows="5"></textarea></label>
<input name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
<button class="btn" type="submit">Send</button>
<p id="consult-msg" class="muted" role="status"></p>
<p class="muted">Prefer to talk? Call <a href="tel:{tel(S['phones'][0])}">{S['phones'][0]}</a>.</p></form>
<script>
document.getElementById("consult").addEventListener("submit", async (e) => {{
  e.preventDefault(); const f = e.target, msg = document.getElementById("consult-msg"), b = f.querySelector("button");
  const d = Object.fromEntries(new FormData(f).entries());
  if (!d.phone && !d.email) {{ msg.textContent = "Please add a phone number or email so we can reach you."; return; }}
  b.disabled = true; msg.textContent = "Sending...";
  try {{
    const r = await fetch("{S['api_base']}/cs/inquiry", {{method: "POST", headers: {{"Content-Type": "application/json"}}, body: JSON.stringify(d)}});
    if (!r.ok) throw new Error(r.status);
    f.reset(); msg.textContent = "Thanks! We got it and will reach out within one business day.";
  }} catch (err) {{
    msg.innerHTML = 'Something went wrong. Please call us or email <a href="mailto:{S['email']}">{S['email']}</a>.';
  }} finally {{ b.disabled = false; }}
}});
</script></section>""")

    shutil.copyfile(os.path.join(OUT, "index.html"), os.path.join(OUT, "404.html"))
    urls = ["/", "/services/", "/find-our-machines/", "/partners/", "/schedule-free-consult/"] + \
           [f"/locations/{slug(l['name'])}/" for l in locs]
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{S['url']}{u}</loc></url>" for u in urls) + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {S['url']}/sitemap.xml\n")
    open(os.path.join(OUT, "CNAME"), "w").write(S["url"].split("//")[1] + "\n")
    print(f"built {len(urls)} pages into {OUT}")


if __name__ == "__main__":
    build()
