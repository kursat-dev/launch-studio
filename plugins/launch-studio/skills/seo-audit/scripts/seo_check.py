#!/usr/bin/env python3
"""On-page SEO checker. Standard library only.

Usage:
  python3 seo_check.py https://example.com/          # live page (+ robots.txt, sitemap)
  python3 seo_check.py dist/index.html               # built file on disk

Prints findings as ERROR / WARN / INFO / OK. Exit code 1 if any ERROR.
It reads one page; it does not crawl the site.
"""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = "launch-studio-seo-check/0.1"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.in_title = "", False
        self.meta, self.links, self.hreflang = {}, {}, []
        self.lang = None
        self.h1, self.h2_count, self.in_h1 = [], 0, False
        self.jsonld, self.in_jsonld, self.buf = [], False, ""
        self.imgs_no_alt, self.imgs = 0, 0
        self.skip_depth, self.text_chars, self.in_body = 0, 0, False

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "body":
            self.in_body = True
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            rel = a.get("rel", "").lower()
            if rel == "alternate" and a.get("hreflang"):
                self.hreflang.append((a["hreflang"], a.get("href", "")))
            elif rel:
                self.links.setdefault(rel, a.get("href", ""))
        elif tag == "h1":
            self.in_h1, self.buf = True, ""
        elif tag == "h2":
            self.h2_count += 1
        elif tag == "img":
            self.imgs += 1
            if "alt" not in a:
                self.imgs_no_alt += 1
        elif tag == "script":
            if a.get("type", "").lower() == "application/ld+json":
                self.in_jsonld, self.buf = True, ""
            self.skip_depth += 1
        elif tag in ("style", "noscript", "template"):
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1" and self.in_h1:
            self.in_h1 = False
            self.h1.append(" ".join(self.buf.split()))
        elif tag == "script":
            if self.in_jsonld:
                self.jsonld.append(self.buf)
                self.in_jsonld = False
            self.skip_depth = max(0, self.skip_depth - 1)
        elif tag in ("style", "noscript", "template"):
            self.skip_depth = max(0, self.skip_depth - 1)

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_h1 or self.in_jsonld:
            self.buf += data
        if self.in_body and not self.skip_depth:
            self.text_chars += len(data.strip())


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read(3_000_000).decode(r.headers.get_content_charset() or "utf-8", "replace")
            return r.status, r.geturl(), dict(r.headers), body
    except urllib.error.HTTPError as e:
        return e.code, url, dict(e.headers or {}), ""


def main(argv):
    if len(argv) != 1:
        print(__doc__)
        return 2
    target = argv[0]
    out = []

    def add(level, msg):
        out.append((level, msg))

    is_url = target.startswith(("http://", "https://"))
    headers, final_url = {}, target
    if is_url:
        try:
            status, final_url, headers, html = fetch(target)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            print(f"ERROR  could not fetch {target}: {e}")
            return 1
        add("OK" if status == 200 else "ERROR", f"HTTP {status}")
        if final_url != target:
            add("INFO", f"redirected to {final_url}")
        if final_url.startswith("http://"):
            add("WARN", "page is served over http, not https")
    else:
        with open(target, encoding="utf-8", errors="replace") as f:
            html = f.read()

    p = PageParser()
    p.feed(html)
    m = p.meta

    title = " ".join(p.title.split())
    if not title:
        add("ERROR", "no <title>")
    else:
        add("WARN" if not 10 <= len(title) <= 60 else "OK", f"title ({len(title)} chars): {title}")

    desc = m.get("description", "").strip()
    if not desc:
        add("WARN", "no meta description")
    else:
        add("WARN" if not 50 <= len(desc) <= 160 else "OK", f"meta description ({len(desc)} chars)")

    if "viewport" not in m:
        add("ERROR", "no meta viewport (page will not be mobile-friendly)")
    add("OK" if p.lang else "WARN", f"<html lang> = {p.lang!r}")

    robots_meta = (m.get("robots", "") + " " + m.get("googlebot", "")).lower()
    x_robots = next((v for k, v in headers.items() if k.lower() == "x-robots-tag"), "").lower()
    if "noindex" in robots_meta or "noindex" in x_robots:
        add("WARN", "noindex is set: right for staging, wrong for a public page")

    canonical = p.links.get("canonical", "")
    if not canonical:
        add("WARN", "no rel=canonical")
    elif not canonical.startswith(("http://", "https://")):
        add("WARN", f"canonical is relative: {canonical} (use an absolute https URL)")
    else:
        add("OK", f"canonical: {canonical}")
        if is_url and canonical.rstrip("/") != final_url.rstrip("/"):
            add("INFO", "canonical differs from the fetched URL (fine if intentional)")

    if len(p.h1) != 1:
        add("WARN", f"{len(p.h1)} <h1> elements (use exactly one): {p.h1[:3]}")
    else:
        add("OK", f"h1: {p.h1[0][:90]}")
    add("INFO", f"{p.h2_count} <h2> elements")

    for key in ("og:title", "og:description", "og:image", "og:url"):
        if not m.get(key):
            add("WARN", f"no {key}")
    og_img = m.get("og:image", "")
    if og_img and not og_img.startswith(("http://", "https://")):
        add("WARN", f"og:image must be an absolute URL: {og_img}")
    if not m.get("twitter:card"):
        add("INFO", "no twitter:card (summary_large_image is a good default)")

    if not p.jsonld:
        add("INFO", "no JSON-LD structured data")
    for block in p.jsonld:
        try:
            data = json.loads(block)
            items = data if isinstance(data, list) else data.get("@graph", [data])
            types = [i.get("@type") for i in items if isinstance(i, dict)]
            add("OK", f"JSON-LD types: {types}")
        except json.JSONDecodeError as e:
            add("ERROR", f"JSON-LD does not parse: {e}")

    for lang, href in p.hreflang:
        if not href.startswith(("http://", "https://")):
            add("WARN", f"hreflang {lang} href is not absolute: {href}")
    if p.hreflang:
        add("INFO", f"hreflang: {[lang for lang, _ in p.hreflang]}")

    if p.imgs_no_alt:
        add("WARN", f"{p.imgs_no_alt} of {p.imgs} <img> have no alt attribute")
    if p.text_chars < 200:
        add("WARN", f"only {p.text_chars} characters of text in the HTML: content is probably rendered by JavaScript; "
                    "pre-render or server-render public pages so search engines and share previews see it")

    if not p.links.get("icon") and not p.links.get("shortcut icon"):
        add("INFO", "no <link rel=icon>")

    if is_url:
        base = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(final_url))
        status, _, _, robots = fetch(base + "/robots.txt")
        sitemaps = []
        if status != 200:
            add("WARN", f"robots.txt: HTTP {status}")
        else:
            agent_all, blocked = False, False
            for line in robots.splitlines():
                k, _, v = line.partition(":")
                k, v = k.strip().lower(), v.strip()
                if k == "user-agent":
                    agent_all = v == "*"
                elif k == "disallow" and agent_all and v == "/":
                    blocked = True
                elif k == "sitemap":
                    sitemaps.append(v)
            add("ERROR" if blocked else "OK", "robots.txt blocks the whole site for *" if blocked else "robots.txt found")
            if not sitemaps:
                add("WARN", "robots.txt does not list a Sitemap:")
        sm_url = sitemaps[0] if sitemaps else base + "/sitemap.xml"
        status, _, _, sm = fetch(sm_url)
        if status != 200:
            add("WARN", f"sitemap {sm_url}: HTTP {status}")
        else:
            add("OK", f"sitemap {sm_url}: {sm.count('<loc>')} URLs")

    order = {"ERROR": 0, "WARN": 1, "INFO": 2, "OK": 3}
    for level, msg in sorted(out, key=lambda x: order[x[0]]):
        print(f"{level:<6} {msg}")
    errors = sum(1 for lvl, _ in out if lvl == "ERROR")
    warns = sum(1 for lvl, _ in out if lvl == "WARN")
    print(f"\n{errors} errors, {warns} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
