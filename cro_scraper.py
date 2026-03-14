import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def scrape_landing_page(url):
    """
    Deep scrape a single landing page for CRO analysis.
    Returns structured content including all copy, CTAs, social proof, and structure.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove non-content elements
        for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
            tag.decompose()

        # --- Navigation links (these are exit risks on prelanders) ---
        nav_links = []
        for nav in soup.find_all(["nav", "header"]):
            for a in nav.find_all("a", href=True):
                text = a.get_text(strip=True)
                if text:
                    nav_links.append(text)

        # --- Page title & meta ---
        title = soup.title.string.strip() if soup.title else ""
        meta_desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            meta_desc = meta.get("content", "")

        # --- Headings hierarchy ---
        headings = []
        for level in ["h1", "h2", "h3", "h4"]:
            for h in soup.find_all(level):
                text = h.get_text(strip=True)
                if text:
                    headings.append({"level": level.upper(), "text": text})

        # --- CTA buttons ---
        ctas = []
        for btn in soup.find_all(["button", "a"]):
            text = btn.get_text(strip=True)
            href = btn.get("href", "")
            classes = " ".join(btn.get("class", []))
            if text and len(text) < 80 and any(kw in text.lower() for kw in [
                "shop", "buy", "order", "get", "upgrade", "start", "claim",
                "try", "add", "checkout", "purchase", "now", "today", "sale"
            ]):
                ctas.append({"text": text, "href": href})

        # --- Social proof signals ---
        full_text = soup.get_text(separator=" ")
        full_text = re.sub(r'\s+', ' ', full_text)

        social_proof = []
        patterns = [
            r'\d[\d,]*\+?\s*(?:sold|customers|reviews?|women|men|people|users)',
            r'\d+\.?\d*\s*/\s*5',
            r'\d+%\s+\w+',
            r'as seen in',
            r'featured in',
            r'\d+-day\s+(?:money[- ]back|guarantee|return)',
            r'\d+[- ]month\s+warranty',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            social_proof.extend(matches[:3])

        # --- Offer / pricing signals ---
        pricing = []
        price_patterns = [
            r'\$[\d,]+\.?\d*',
            r'\d+%\s+off',
            r'free\s+shipping',
            r'save\s+\$[\d,]+',
        ]
        for pattern in price_patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            pricing.extend(matches[:4])

        # --- Video embeds detected ---
        videos = []
        for v in soup.find_all(["video", "iframe"]):
            src = v.get("src", v.get("data-src", ""))
            if src:
                videos.append(src[:100])
        # Also check for video file links in anchors
        for a in soup.find_all("a", href=True):
            if ".mp4" in a["href"] or "video" in a["href"].lower():
                videos.append(a["href"][:100])

        # --- Full body copy (clean) ---
        main = soup.find("main") or soup.find(id="MainContent") or soup.body
        if main:
            # Remove nav/header/footer from main too
            for tag in main.find_all(["nav", "header", "footer"]):
                tag.decompose()
            body_text = re.sub(r'\s+', ' ', main.get_text(separator=" ")).strip()
        else:
            body_text = full_text

        # --- FAQ sections ---
        faqs = []
        faq_containers = soup.find_all(attrs={"class": re.compile(r"faq|accordion|collapse", re.I)})
        for container in faq_containers[:5]:
            text = container.get_text(separator=" ", strip=True)
            if text:
                faqs.append(text[:300])

        return {
            "ok": True,
            "url": url,
            "title": title,
            "meta_description": meta_desc,
            "nav_links": list(set(nav_links))[:10],
            "headings": headings[:20],
            "ctas": ctas[:10],
            "social_proof": list(set(social_proof))[:10],
            "pricing": list(set(pricing))[:8],
            "videos_detected": videos[:5],
            "faq_snippets": faqs,
            "body_text": body_text[:5000],
        }

    except Exception as e:
        return {"ok": False, "url": url, "error": str(e)}


def format_for_prompt(scraped):
    """Convert scraped data into a structured string for the LLM prompt."""
    if not scraped.get("ok"):
        return f"ERROR: Could not scrape {scraped['url']}: {scraped.get('error')}"

    lines = [
        f"URL: {scraped['url']}",
        f"Page title: {scraped['title']}",
        "",
        "=== NAVIGATION LINKS (exit risks) ===",
        ", ".join(scraped["nav_links"]) if scraped["nav_links"] else "None detected",
        "",
        "=== HEADING HIERARCHY ===",
    ]
    for h in scraped["headings"]:
        lines.append(f"  {h['level']}: {h['text']}")

    lines += [
        "",
        "=== CTA BUTTONS DETECTED ===",
    ]
    for cta in scraped["ctas"]:
        lines.append(f"  - \"{cta['text']}\" → {cta['href'][:60] if cta['href'] else 'no href'}")

    lines += [
        "",
        "=== SOCIAL PROOF SIGNALS ===",
        "\n".join(f"  - {s}" for s in scraped["social_proof"]) if scraped["social_proof"] else "  None detected",
        "",
        "=== PRICING / OFFER SIGNALS ===",
        "\n".join(f"  - {p}" for p in scraped["pricing"]) if scraped["pricing"] else "  None detected",
        "",
        "=== VIDEO ASSETS ===",
        f"  {len(scraped['videos_detected'])} video(s) detected" if scraped["videos_detected"] else "  None detected",
    ]

    if scraped["faq_snippets"]:
        lines += ["", "=== FAQ CONTENT (first entries) ==="]
        for faq in scraped["faq_snippets"][:2]:
            lines.append(f"  {faq[:200]}")

    lines += [
        "",
        "=== FULL PAGE COPY ===",
        scraped["body_text"],
    ]

    return "\n".join(lines)
