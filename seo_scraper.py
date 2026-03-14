import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Pages to crawl beyond the homepage
PRIORITY_PATHS = [
    "/",
    "/pages/our-story",
    "/pages/about",
    "/pages/american-castle",
    "/collections/all",
    "/products/angle-grinder",
    "/products/rotary-hammer",
    "/products/survival-flashlight",
    "/blogs",
    "/pages/contact",
]


def scrape_page(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Title & meta
        title = soup.title.string.strip() if soup.title else ""
        meta_desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            meta_desc = meta.get("content", "")

        # OG tags
        og_title = ""
        og = soup.find("meta", property="og:title")
        if og:
            og_title = og.get("content", "")

        # Heading hierarchy
        headings = []
        for level in ["h1", "h2", "h3"]:
            for h in soup.find_all(level):
                text = h.get_text(strip=True)
                if text:
                    headings.append({"level": level.upper(), "text": text})

        # Internal links + anchor text
        internal_links = []
        base_domain = urlparse(url).netloc
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            full = urljoin(url, href)
            if urlparse(full).netloc == base_domain and text:
                internal_links.append({"href": full, "text": text[:80]})

        # Schema markup detection
        schema_types = []
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                import json
                data = json.loads(script.string or "{}")
                t = data.get("@type", "")
                if t:
                    schema_types.append(t if isinstance(t, str) else str(t))
            except Exception:
                pass

        # Word count
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        body_text = re.sub(r"\s+", " ", soup.get_text(separator=" ")).strip()
        word_count = len(body_text.split())

        return {
            "ok": True,
            "url": url,
            "title": title,
            "meta_description": meta_desc,
            "og_title": og_title,
            "headings": headings[:20],
            "internal_links": internal_links[:30],
            "schema_types": schema_types,
            "word_count": word_count,
            "body_text": body_text[:4000],
        }
    except Exception as e:
        return {"ok": False, "url": url, "error": str(e)}


def check_robots_txt(base_url):
    """Check robots.txt for AI crawler permissions."""
    try:
        url = base_url.rstrip("/") + "/robots.txt"
        resp = requests.get(url, headers=HEADERS, timeout=8)
        content = resp.text.lower()
        return {
            "ok": True,
            "raw": resp.text[:800],
            "gptbot_blocked": "gptbot" in content and "disallow" in content.split("gptbot")[1][:50],
            "bingbot_blocked": "bingbot" in content and "disallow" in content.split("bingbot")[1][:50] if "bingbot" in content else False,
            "has_sitemap": "sitemap" in content,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def check_sitemap(base_url):
    """Check if sitemap exists and is accessible."""
    for path in ["/sitemap.xml", "/sitemap_index.xml"]:
        try:
            url = base_url.rstrip("/") + path
            resp = requests.get(url, headers=HEADERS, timeout=8)
            if resp.status_code == 200 and "xml" in resp.headers.get("content-type", ""):
                urls = re.findall(r"<loc>(.*?)</loc>", resp.text)
                return {"ok": True, "url": url, "url_count": len(urls)}
        except Exception:
            pass
    return {"ok": False}


def scrape_seo_site(base_url):
    """
    Full SEO crawl: homepage + priority pages + robots + sitemap.
    Returns structured data for the SEO analysis prompt.
    """
    base_url = base_url.rstrip("/")
    if not base_url.startswith("http"):
        base_url = "https://" + base_url

    results = {"pages": {}, "robots": {}, "sitemap": {}}

    # Robots.txt
    results["robots"] = check_robots_txt(base_url)

    # Sitemap
    results["sitemap"] = check_sitemap(base_url)

    # Crawl pages
    for path in PRIORITY_PATHS:
        url = base_url + path
        data = scrape_page(url)
        if data["ok"]:
            key = path.strip("/").replace("/", "_") or "homepage"
            results["pages"][key] = data
        time.sleep(0.4)
        if len(results["pages"]) >= 6:
            break

    return results


def format_seo_for_prompt(scraped, target_keyword):
    """Format scraped SEO data as a structured string for the LLM prompt."""
    lines = [f"TARGET KEYWORD: {target_keyword}", ""]

    # Robots
    robots = scraped.get("robots", {})
    if robots.get("ok"):
        lines += [
            "=== ROBOTS.TXT ===",
            f"GPTBot blocked: {robots.get('gptbot_blocked', 'unknown')}",
            f"Bingbot blocked: {robots.get('bingbot_blocked', 'unknown')}",
            f"Sitemap declared: {robots.get('has_sitemap', False)}",
            "",
        ]

    # Sitemap
    sitemap = scraped.get("sitemap", {})
    lines += [
        "=== SITEMAP ===",
        f"Found: {sitemap.get('ok', False)} — {sitemap.get('url_count', 0)} URLs indexed" if sitemap.get("ok") else "Sitemap: not found or inaccessible",
        "",
    ]

    # Pages
    for key, page in scraped.get("pages", {}).items():
        if not page.get("ok"):
            continue
        lines += [
            f"=== PAGE: {page['url']} ===",
            f"Title tag: {page['title'] or 'MISSING'}",
            f"Meta description: {page['meta_description'] or 'MISSING'}",
            f"Word count: {page['word_count']}",
            f"Schema types detected: {', '.join(page['schema_types']) if page['schema_types'] else 'NONE'}",
        ]
        for h in page["headings"][:8]:
            lines.append(f"  {h['level']}: {h['text']}")

        nav_anchors = [l["text"] for l in page["internal_links"][:10] if l["text"]]
        if nav_anchors:
            lines.append(f"Nav/internal anchor text: {', '.join(nav_anchors[:8])}")
        lines.append("")

    return "\n".join(lines)
