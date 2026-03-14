# AI Growth Audit Dashboard

A conversion rate optimization (CRO) agent built with Streamlit and Claude. Scrapes a landing page, builds a structured prompt using the `page-cro` skill, calls the Anthropic API, and returns a full audit with A/B test recommendations, copy rewrites, tracking plans, and retargeting cohorts.

Built for the SRI Labs & Cyber Power Tools marketing assessment.

---

## What It Does

1. **Scrapes** the landing page — extracts headings, CTAs, social proof, pricing signals, video assets, and full body copy
2. **Builds a prompt** using the `page-cro` marketingskills skill as the system context
3. **Calls Claude** via the Anthropic API — twice (CRO analysis + copy deep-dive)
4. **Renders results** across 5 tabs:
   - CRO Tests — prioritized A/B tests with control/variant and expected lift
   - Copy Rewrites — current vs. rewritten copy for each page element
   - Copy Variants — 3 full hero section rewrites, A/B test ready
   - Tracking Plan — video events, CTA events, scroll depth, engagement signals, retargeting cohorts
   - Structural Issues — critical, warning, and minor fixes

---

## Files

```
cro_agent.py      — Streamlit app, UI, and result rendering
cro_scraper.py    — Landing page scraper and content extractor
cro_prompts.py    — LLM prompt builder (system prompt + CRO + copy prompts)
requirements.txt  — Python dependencies
```

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/sophiasanh/ai-growth-audit-dasboard
cd ai-growth-audit-dasboard
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**

Create a `.env` file in the project root — this file is gitignored and stays on your machine:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Or export it directly in your terminal:
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**4. Run the app**
```bash
streamlit run cro_agent.py
```

Opens at `http://localhost:8501`

---

## Deploy to Streamlit Cloud

1. Push all files to this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app**
4. Select this repo, branch `main`, main file `cro_agent.py`
5. Click **Advanced settings → Secrets** and paste:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

6. Click **Deploy**

Your API key is stored encrypted in Streamlit's servers — it never touches the repo.

---

## Demo Inputs

Use these inputs to run the full CRO audit in the demo:

| Field | Value |
|---|---|
| URL | `https://srilabs.com/pages/sri-dryq-fb-prelander` |
| Traffic source | `Meta Ads (Facebook/Instagram)` |
| Target audience | `Women 35–65` |
| Conversion goal | `Purchase DryQ hair dryer` |
| Video context | `Hero video: FOX 5 Localist SD host Ashley Jacobs endorses DryQ red light therapy for hair growth. ~3 min earned media news feature. Primary trust asset on the page. Second video mid-page: "What you should know about SRI DryQ" — product explainer.` |

---

## How the Agent Works

```
User inputs URL + context
        ↓
cro_scraper.py  →  scrapes live page, extracts structured data
        ↓
cro_prompts.py  →  builds two prompts:
                   1. CRO analysis prompt (page-cro skill as system context)
                   2. Copy deep-dive prompt
        ↓
Anthropic API   →  claude-sonnet-4-20250514, two calls
        ↓
cro_agent.py    →  parses JSON responses, renders 5-tab dashboard
```

The `TRACKING_EVENT_TAXONOMY` in `cro_prompts.py` defines 22 named events across four categories. These are injected into the prompt so Claude uses consistent, pre-defined event names rather than inventing its own — making the output ready to hand directly to a developer.

---

## Skills Used

From the [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) agent pack:

- `page-cro` — conversion rate optimization framework
- `ab-test-setup` — A/B test structure and hypothesis format
- `copywriting` — direct response copy for ecommerce
- `analytics-tracking` — event taxonomy and retargeting cohort logic

---

## Security

- API key is never stored in code
- Loaded from environment variable: `os.environ.get("ANTHROPIC_API_KEY")`
- For local dev: use a `.env` file (gitignored)
- For Streamlit Cloud: use the Secrets panel
- `.gitignore` blocks `.env` and `secrets.toml` from being committed
