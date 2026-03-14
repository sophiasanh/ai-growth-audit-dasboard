"""
SEO Agent Prompts
Built from the ai-seo + schema-markup + programmatic-seo marketingskills skill context.
"""

SEO_SYSTEM_PROMPT = """You are a senior SEO strategist specializing in ecommerce and small business websites. You combine traditional on-page SEO with AI discoverability (AEO/GEO) — optimizing for both Google rankings and LLM citations.

Your expertise covers:
- On-page keyword optimization: title tags, H1, meta descriptions, body copy
- Schema markup: Organization, Product, FAQ, BreadcrumbList, VideoObject
- Topical authority: pillar pages, content clusters, internal linking strategy
- AI discoverability: robots.txt for AI crawlers, FAQ citation engines, extractable content formats
- Programmatic SEO: supporting page templates, keyword cluster mapping

Your framework (from the ai-seo skill):
1. Technical foundation — can search engines and AI crawlers access and read the site?
2. Keyword signal — does the page clearly tell crawlers what it's about?
3. Topical authority — does the site have enough content depth to rank for category terms?
4. Schema layer — is structured data present to unlock rich results and AI citations?
5. Content extractability — is content formatted for AI to quote and cite?

Output only valid JSON. No markdown, no preamble."""


# Supporting page templates injected into the prompt
SUPPORTING_PAGE_TEMPLATES = """
REQUIRED SUPPORTING PAGES (build these to establish topical authority):

Page 1: Best Cyber Tools for Contractors
- URL: /blogs/best-cyber-tools-contractors
- Intent: Commercial — buyers researching before purchasing
- Target keywords: best cyber tools for contractors, professional cyber tools
- Required sections: Introduction, Top picks with specs, Use case breakdown, FAQ

Page 2: Cyber Tools vs Traditional Power Tools
- URL: /blogs/cyber-tools-vs-traditional
- Intent: Informational/Commercial — comparison shoppers
- Target keywords: cyber tools vs traditional power tools, are cyber tools worth it
- Required sections: Side-by-side comparison table, Key differences, Who should choose each, FAQ

Page 3: Complete Guide to Cyber Tools (Pillar Page)
- URL: /blogs/complete-guide-cyber-tools
- Intent: Informational — topical authority hub
- Target keywords: cyber tools, complete guide to cyber tools, what are cyber tools
- Required sections: What are cyber tools, The full product lineup, Technology explained, Buyer's guide, FAQ
- This page links to all PDPs and both supporting pages above
"""


def build_seo_prompt(scraped_content, target_keyword, site_url):
    return f"""Analyze this website for SEO optimization. Apply the full ai-seo + schema-markup + programmatic-seo skill framework.

SITE URL: {site_url}
PRIMARY TARGET KEYWORD: {target_keyword}
GOAL: Rank page-1 on Google for "{target_keyword}" and appear in AI search citations

{SUPPORTING_PAGE_TEMPLATES}

--- SCRAPED SITE DATA ---
{scraped_content}
--- END SCRAPED DATA ---

Return a JSON object with EXACTLY this structure:

{{
  "seo_audit": {{
    "overall_score": 0,
    "score_reasoning": "2-3 sentence summary of current SEO health and biggest opportunity",
    "keyword_signal_score": "1-10",
    "technical_health": "good|fair|poor",
    "estimated_time_to_rank": "e.g. 60-90 days with these fixes",
    "quick_wins": ["fix that takes less than 1 day", "string", "string"]
  }},
  "on_page_fixes": [
    {{
      "element": "Title tag | H1 | Meta description | Body copy | Nav anchor text",
      "page": "Homepage | /products/angle-grinder | etc.",
      "current": "Exact current text or MISSING",
      "recommended": "Your exact recommended replacement",
      "reason": "Why this change helps rank for the target keyword",
      "priority": "P1|P2|P3",
      "effort": "low|medium|high"
    }}
  ],
  "schema_plan": [
    {{
      "schema_type": "Organization | Product | FAQ | BreadcrumbList | VideoObject | HowTo",
      "page": "Which page to add it to",
      "priority": "critical|high|medium",
      "ai_impact": "How this schema helps with AI citations specifically",
      "json_ld_outline": {{}}
    }}
  ],
  "supporting_pages": [
    {{
      "title": "string",
      "url_slug": "string",
      "target_keywords": ["string"],
      "intent": "commercial|informational|transactional",
      "required_sections": ["string"],
      "word_count_target": 0,
      "internal_links_to": ["string — which existing pages to link to"],
      "why_it_builds_authority": "string"
    }}
  ],
  "keyword_cluster": [
    {{
      "keyword": "string",
      "monthly_volume": "string",
      "difficulty": "low|medium|high",
      "intent": "commercial|informational|transactional|brand",
      "target_page": "string",
      "current_gap": "string — what's missing to rank for this"
    }}
  ],
  "ai_discoverability": {{
    "robots_txt_status": "pass|fail|unknown",
    "gptbot_access": "allowed|blocked|unknown",
    "bingbot_access": "allowed|blocked|unknown",
    "bing_webmaster_action": "string — what to do",
    "faq_citation_entries": [
      {{
        "question": "string — a question users ask AI about this brand or product category",
        "answer": "string — direct answer optimized for AI citation, under 3 sentences",
        "page_to_add_to": "string"
      }}
    ],
    "content_extractability_gaps": ["string — what's missing that prevents AI from citing this site"]
  }},
  "thirty_sixty_ninety": {{
    "day_30": {{
      "theme": "string",
      "actions": ["string"]
    }},
    "day_60": {{
      "theme": "string",
      "actions": ["string"]
    }},
    "day_90": {{
      "theme": "string",
      "actions": ["string"]
    }}
  }}
}}

Rules:
- on_page_fixes must have 5-8 items, P1 first
- schema_plan must include Organization and at least 2 others
- supporting_pages must have exactly 3 items matching the templates above
- keyword_cluster must have 6-8 keywords
- faq_citation_entries must have 4-5 entries
- All recommended copy must naturally contain the target keyword "{target_keyword}"
- Return only the JSON object"""
