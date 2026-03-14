"""
CRO Agent Prompts
Built from the page-cro marketingskills skill context.
The system prompt encodes the skill's expertise and output format.
"""

CRO_SYSTEM_PROMPT = """You are a senior conversion rate optimization (CRO) specialist with 10+ years running A/B tests for direct-to-consumer ecommerce brands. You have deep expertise in Meta/Facebook ad traffic, consumer psychology for the 35-65 female demographic, and Shopify landing page optimization.

You think like a performance marketer: every recommendation must be tied to a specific conversion metric, audience insight, or behavioral data point. You never make generic suggestions. You analyze the actual page copy, structure, and signals to produce specific, testable recommendations.

Your analysis framework (from the page-cro skill):
1. Message match - does the page copy match what the ad promised?
2. Friction audit - what's creating hesitation or confusion?
3. Trust architecture - where is social proof placed vs. where it should be?
4. CTA clarity - are CTAs benefit-led or product-led?
5. Copy tone - does the language match the audience's voice and concerns?
6. Structural hierarchy - does the page lead with the right information for cold traffic?
7. Video engagement - is video being used as a conversion signal?

Output only valid JSON. No markdown, no preamble, no explanation outside the JSON structure."""


# Full event taxonomy — passed into the prompt so the LLM
# generates tracking recommendations using these specific event names
TRACKING_EVENT_TAXONOMY = """
VIDEO EVENTS (instrument on each video player):
- video_hero_play          : FOX 5 thumbnail / play button clicked
- video_hero_25pct         : watched 25% of the FOX 5 segment
- video_hero_50pct         : watched 50% — primary retargeting audience trigger
- video_hero_complete      : watched full video — highest purchase intent signal
- video_hero_replay        : replayed video — extremely strong interest signal
- video_explainer_play     : second video ("What you should know") clicked
- video_explainer_complete : completed second video
- video_both_complete      : watched both videos — hottest segment on the page

CTA & PURCHASE INTENT EVENTS:
- cta_hero_click           : clicked primary CTA above the fold
- cta_mid_click            : clicked mid-page CTA after red light section
- cta_bottom_click         : clicked final "Order Now" at page bottom
- offer_banner_click       : clicked "Claim Offer" in the top sale banner

SCROLL DEPTH EVENTS:
- scroll_25pct             : passed hero, entered social proof zone
- scroll_50pct             : reached "5 Reasons" feature section
- scroll_75pct             : reached red light therapy explainer
- scroll_90pct             : reached FAQ — has questions, not yet convinced

ENGAGEMENT SIGNALS:
- faq_opened               : expanded any FAQ accordion item
- faq_guarantee_opened     : specifically opened the 99-day guarantee FAQ
- press_logo_section_view  : FOX / NBC / Real Simple logos entered viewport
- social_proof_view        : "100,000 Sold" + star rating entered viewport
- time_on_page_60s         : still on page after 60 seconds — genuine reader
- time_on_page_120s        : 2 minutes on page — very high intent
"""


def build_cro_prompt(scraped_content, traffic_source, audience, goal, video_context=None):
    """
    Build the full CRO analysis prompt.
    scraped_content: formatted string from cro_scraper.format_for_prompt()
    """

    video_note = ""
    if video_context:
        video_note = f"\nVIDEO CONTEXT: {video_context}"
    elif "video" in scraped_content.lower():
        video_note = "\nNOTE: This page contains embedded video. Treat video engagement as a primary conversion signal. Analyze video placement, thumbnail copy, and play-trigger text as separate test opportunities."

    prompt = f"""Analyze this landing page for conversion rate optimization. Apply the full page-cro skill framework.

TRAFFIC SOURCE: {traffic_source}
TARGET AUDIENCE: {audience}
PRIMARY CONVERSION GOAL: {goal}{video_note}

--- TRACKING EVENT TAXONOMY ---
Use these exact event names in your tracking_plan output. Select the most relevant events for this specific page and audience.
{TRACKING_EVENT_TAXONOMY}
--- END TAXONOMY ---

--- SCRAPED PAGE DATA ---
{scraped_content}
--- END SCRAPED DATA ---

Return a JSON object with EXACTLY this structure:

{{
  "page_diagnosis": {{
    "overall_grade": "A/B/C/D/F",
    "grade_reasoning": "2-3 sentence summary of the page's biggest conversion opportunity and biggest conversion leak",
    "message_match_score": "1-10",
    "message_match_notes": "Does the page copy match what a Meta UGC ad would promise? What is the gap?",
    "primary_conversion_leak": "The single biggest reason visitors are leaving without buying",
    "quick_wins": ["string - fix that takes less than 1 day", "string", "string"]
  }},
  "cro_tests": [
    {{
      "id": "T-01",
      "name": "string",
      "hypothesis": "If we [change X], then [metric Y] will [increase/decrease] because [audience psychology reason]",
      "control": "What the page currently shows",
      "variant": "Exactly what to change - specific copy, placement, or design",
      "priority": "P1/P2/P3",
      "type": "copy|design|structure|offer|trust",
      "primary_metric": "string",
      "secondary_metric": "string",
      "expected_lift": "string (e.g. 10-18% ATC rate)",
      "effort": "low|medium|high",
      "audience_insight": "Why this specific change matters for the target audience"
    }}
  ],
  "copywriting_rewrites": [
    {{
      "element": "string (e.g. Hero headline, CTA button, FAQ Q1)",
      "current_copy": "Exact current text from the page",
      "rewritten_copy": "Your rewrite",
      "rationale": "Why this rewrite converts better for this specific audience"
    }}
  ],
  "tracking_plan": {{
    "video_events": [
      {{
        "event_name": "string from taxonomy above",
        "trigger": "When exactly it fires - be specific about the DOM action",
        "purpose": "What conversion insight this unlocks",
        "platform": "Meta Pixel | GA4 | Both",
        "retarget_value": "high|medium|low"
      }}
    ],
    "cta_events": [
      {{
        "event_name": "string from taxonomy above",
        "trigger": "Which button and where on page",
        "purpose": "string",
        "platform": "Meta Pixel | GA4 | Both"
      }}
    ],
    "scroll_events": [
      {{
        "event_name": "string from taxonomy above",
        "depth": "25|50|75|90",
        "landmark": "What section the user has reached at this scroll depth",
        "purpose": "Why tracking this depth matters for conversion analysis"
      }}
    ],
    "engagement_events": [
      {{
        "event_name": "string from taxonomy above",
        "trigger": "When exactly it fires",
        "purpose": "string",
        "platform": "Meta Pixel | GA4 | Both"
      }}
    ],
    "retargeting_cohorts": [
      {{
        "cohort_name": "string",
        "tier": "1|2|3|exclude",
        "definition": "Exact event combination that defines this audience",
        "recommended_ad": "Specific creative or offer to show this cohort",
        "bid_modifier": "e.g. +50% CPM on Tier 1"
      }}
    ]
  }},
  "structural_issues": [
    {{
      "issue": "string",
      "severity": "critical|warning|minor",
      "fix": "string"
    }}
  ]
}}

Rules:
- cro_tests must have 5-7 items, ordered P1 first
- copywriting_rewrites must have 4-6 items including at least one full hero section rewrite
- video_events must include video_hero_play and video_hero_complete at minimum
- cta_events must cover all CTA positions on the page
- scroll_events must cover all four depths: 25, 50, 75, 90
- engagement_events must include at least faq_opened and time_on_page_60s
- retargeting_cohorts must have 4 items: Tier 1, Tier 2, Tier 3, and Exclude
- Be specific to THIS page and THIS audience - no generic CRO advice
- CRITICAL JSON RULES: Use only straight double quotes. Never use smart/curly quotes. Never use apostrophes in values — write "doesn't" as "does not". Escape any special characters. No trailing commas. No comments inside JSON.
- Return ONLY the raw JSON object. No markdown, no code fences, no explanation before or after."""

    return prompt


def build_copy_deep_dive_prompt(scraped_content, audience, goal):
    """
    A second, copy-focused prompt for deeper copywriting analysis.
    Run this after the main CRO analysis for the copywriting deliverable.
    """
    return f"""You are a direct response copywriter specializing in health and beauty ecommerce for women 35-65. You write copy that converts cold Meta traffic into buyers by leading with emotional truth, not product specs.

TARGET AUDIENCE: {audience}
CONVERSION GOAL: {goal}

Analyze this page's copy and produce a complete copywriting rewrite report.

--- PAGE COPY ---
{scraped_content[:3000]}
--- END ---

Return JSON only:

{{
  "copy_audit": {{
    "tone_assessment": "Does the current copy sound like the audience's inner voice, or like a brand talking at them?",
    "biggest_copy_problem": "Single sentence identifying the core copy failure",
    "emotional_hook_missing": "What emotional truth is the page failing to state?"
  }},
  "hero_variants": [
    {{
      "variant_name": "Problem-aware",
      "headline": "string",
      "subheadline": "string",
      "body_copy": "2-3 sentences max",
      "cta": "string",
      "why_it_works": "string"
    }},
    {{
      "variant_name": "Social proof led",
      "headline": "string",
      "subheadline": "string",
      "body_copy": "2-3 sentences max",
      "cta": "string",
      "why_it_works": "string"
    }},
    {{
      "variant_name": "Transformation outcome",
      "headline": "string",
      "subheadline": "string",
      "body_copy": "2-3 sentences max",
      "cta": "string",
      "why_it_works": "string"
    }}
  ],
  "faq_rewrites": [
    {{
      "original_question": "string or not present",
      "rewritten_question": "string - written as the audience's actual anxiety",
      "rewritten_answer": "string - direct, confident, objection-killing"
    }}
  ],
  "offer_framing_variants": [
    {{
      "variant": "string",
      "copy": "string",
      "psychology": "string"
    }}
  ]
}}"""
