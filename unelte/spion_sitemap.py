"""Agentul care urmărește legal SEO-ul concurenței: ce pagini noi a publicat un site (tactica #17).

Citește doar ce site-ul publică singur pentru motoarele de căutare: robots.txt și sitemap-urile declarate
acolo (sau /sitemap.xml). Nu parcurge paginile, nu ocolește nimic, o cerere pe secundă, maximum 25 de
sitemap-uri. Salvează o fotografie a listei de URL-uri și, la rularea următoare, arată ce a apărut, ce a
dispărut și ce s-a actualizat (lastmod). Gratuit, fără cont, fără chei.

Run:  python spion_sitemap.py exemplu.ro [alt-site.ro ...] [--dir .tmp/sitemap_spion]
"""
import argparse
import gzip
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

import requests

UA = "Mozilla/5.0 (compatible; sitemap-check/1.0)"
MAX_SITEMAPS = 25
PAUZA_S = 1.0
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def _get(url: str, sesiune) -> bytes:
    r = sesiune.get(url, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    data = r.content
    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data


def sitemaps_din_robots(text: str, baza: str) -> list:
    out = []
    for ln in text.splitlines():
        m = re.match(r"(?i)^\s*sitemap\s*:\s*(\S+)", ln)
        if m:
            out.append(urljoin(baza, m.group(1)))
    return out


def citeste_sitemap(xml: bytes) -> tuple:
    """(urls {loc: lastmod}, sitemap-uri copil) dintr-un urlset sau sitemapindex."""
    root = ET.fromstring(xml)
    urls, copii = {}, []
    tag = root.tag.replace(NS, "")
    if tag == "sitemapindex":
        for sm in root.iter(f"{NS}sitemap"):
            loc = sm.findtext(f"{NS}loc")
            if loc:
                copii.append(loc.strip())
    else:
        for u in root.iter(f"{NS}url"):
            loc = u.findtext(f"{NS}loc")
            if loc:
                urls[loc.strip()] = (u.findtext(f"{NS}lastmod") or "").strip()
    return urls, copii


def fotografie(site: str, sesiune=None, pauza: float = PAUZA_S) -> dict:
    sesiune = sesiune or requests.Session()
    baza = site if site.startswith("http") else f"https://{site}"
    baza = baza.rstrip("/") + "/"
    try:
        coada = sitemaps_din_robots(_get(urljoin(baza, "robots.txt"), sesiune).decode("utf-8", "replace"), baza)
    except requests.RequestException:
        coada = []
    if not coada:
        coada = [urljoin(baza, "sitemap.xml")]
    urls, vazute = {}, set()
    while coada and len(vazute) < MAX_SITEMAPS:
        sm = coada.pop(0)
        if sm in vazute:
            continue
        vazute.add(sm)
        try:
            u, copii = citeste_sitemap(_get(sm, sesiune))
        except (requests.RequestException, ET.ParseError, OSError) as e:
            print(f"  {sm}: {e}", file=sys.stderr)
            continue
        urls.update(u)
        coada.extend(c for c in copii if c not in vazute)
        time.sleep(pauza)
    return {"site": baza, "data": date.today().isoformat(), "sitemaps": sorted(vazute), "urls": urls}


def diferente(vechi: dict, nou: dict) -> dict:
    a, b = vechi.get("urls", {}), nou.get("urls", {})
    return {"noi": sorted(set(b) - set(a)), "disparute": sorted(set(a) - set(b)),
            "actualizate": sorted(u for u in set(a) & set(b) if a[u] and b[u] and a[u] != b[u])}


def raport(nou: dict, dif: dict, vechi_data: str) -> str:
    L = [f"## {nou['site']} ({nou['data']})", f"{len(nou['urls'])} pagini în sitemap."]
    if not vechi_data:
        L.append("Prima fotografie; diferențele apar de la rularea următoare.")
        return "\n".join(L)
    L.append(f"Față de {vechi_data}: {len(dif['noi'])} noi, {len(dif['actualizate'])} actualizate, {len(dif['disparute'])} dispărute.")
    for k, titlu in (("noi", "Pagini noi"), ("actualizate", "Actualizate"), ("disparute", "Dispărute")):
        if dif[k]:
            L.append(f"\n**{titlu}:**")
            L += [f"- {u}" for u in dif[k][:40]]
            if len(dif[k]) > 40:
                L.append(f"- ... și încă {len(dif[k]) - 40}")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("site", nargs="+")
    ap.add_argument("--dir", default=str(Path(__file__).resolve().parents[4] / ".tmp" / "sitemap_spion"))
    a = ap.parse_args()
    d = Path(a.dir)
    d.mkdir(parents=True, exist_ok=True)
    for site in a.site:
        nume = re.sub(r"[^a-z0-9.-]", "_", site.lower().replace("https://", "").replace("http://", "").strip("/"))
        f = d / f"{nume}.json"
        vechi = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
        nou = fotografie(site)
        print(raport(nou, diferente(vechi, nou), vechi.get("data", "")))
        f.write_text(json.dumps(nou, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
