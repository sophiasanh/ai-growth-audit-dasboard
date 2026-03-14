import streamlit as st
import anthropic
import json
import os
from seo_scraper import scrape_seo_site, format_seo_for_prompt
from seo_prompts import SEO_SYSTEM_PROMPT, build_seo_prompt

st.set_page_config(
    page_title="SEO Agent — Cyber Power Tools",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #08090d !important; color: #dde1ec; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 5rem; max-width: 1100px; }
section[data-testid="stSidebar"] { display: none; }

.topbar { display:flex; align-items:center; justify-content:space-between; padding-bottom:20px; border-bottom:1px solid #1c2030; margin-bottom:28px; }
.tb-left { display:flex; flex-direction:column; gap:3px; }
.tb-title { font-size:15px; font-weight:700; color:#fff; display:flex; align-items:center; gap:10px; }
.tb-dot { width:8px; height:8px; border-radius:50%; background:#5b8ef5; box-shadow:0 0 8px #5b8ef5; animation:pulse 2.4s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.2} }
.tb-sub { font-size:12px; color:#6b7385; }
.tb-badges { display:flex; gap:6px; }
.tb-badge { font-family:'JetBrains Mono',monospace; font-size:10px; padding:3px 10px; border-radius:4px; border:1px solid; }
.tb-badge.blue { color:#5b8ef5; background:rgba(91,142,245,.07); border-color:rgba(91,142,245,.2); }
.tb-badge.teal { color:#22d3b8; background:rgba(34,211,184,.07); border-color:rgba(34,211,184,.2); }
.tb-badge.purple { color:#9d79f5; background:rgba(157,121,245,.07); border-color:rgba(157,121,245,.2); }

.pipe-row { display:flex; align-items:center; margin-bottom:20px; }
.ps { font-size:11px; padding:6px 12px; background:#0f1117; border:1px solid #1c2030; color:#6b7385; font-family:monospace; }
.ps:first-child { border-radius:6px 0 0 6px; }
.ps:last-child { border-radius:0 6px 6px 0; }
.ps.done { background:rgba(52,201,126,.07); border-color:rgba(52,201,126,.25); color:#34c97e; }
.ps.active { border-color:#5b8ef5; color:#5b8ef5; }
.pa { color:#2e3548; font-size:13px; background:#08090d; border-top:1px solid #1c2030; border-bottom:1px solid #1c2030; padding:6px 3px; }

.field label { font-size:11px; color:#6b7385; margin-bottom:4px; display:block; font-family:monospace; }
.run-btn-wrap { display:flex; align-items:flex-end; padding-bottom:1px; }

.score-strip { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:24px; }
.sc { background:#0f1117; border:1px solid #1c2030; border-radius:10px; padding:14px 16px; }
.sc-n { font-size:26px; font-weight:500; line-height:1; margin-bottom:4px; }
.sc-l { font-size:10px; color:#6b7385; text-transform:uppercase; letter-spacing:.08em; }
.blue-c { color:#5b8ef5; } .teal-c { color:#22d3b8; } .amber-c { color:#BA7517; } .green-c { color:#3B6D11; }

.scrape-info { background:#0f1117; border:1px solid #1c2030; border-radius:9px; padding:0 16px; margin-bottom:20px; }
.s-row { display:flex; justify-content:space-between; font-size:12px; padding:8px 0; border-bottom:1px solid #1c2030; }
.s-row:last-child { border-bottom:none; }
.s-key { color:#6b7385; }
.s-val { color:#dde1ec; font-family:'JetBrains Mono',monospace; font-size:11px; }
.s-val.pass { color:#34c97e; }
.s-val.fail { color:#ef5050; }
.s-val.warn { color:#f0a500; }

.diag-card { background:#0f1117; border:1px solid #1c2030; border-radius:12px; padding:18px 22px; margin-bottom:20px; display:flex; gap:18px; align-items:flex-start; }
.score-ring { width:60px; height:60px; border-radius:50%; border:2.5px solid #5b8ef5; display:flex; align-items:center; justify-content:center; font-size:18px; font-weight:500; color:#5b8ef5; flex-shrink:0; }
.diag-meta .dt { font-size:14px; font-weight:500; color:#fff; margin-bottom:5px; }
.diag-meta .dd { font-size:13px; color:#6b7385; line-height:1.65; }
.diag-meta .de { font-size:12px; color:#22d3b8; margin-top:6px; }

.sec-label { font-size:10px; font-weight:500; text-transform:uppercase; letter-spacing:.1em; margin:20px 0 10px; display:flex; align-items:center; gap:8px; }
.sec-label::before { content:''; width:14px; height:1px; display:block; }
.sec-label.blue { color:#5b8ef5; } .sec-label.blue::before { background:#5b8ef5; }
.sec-label.teal { color:#22d3b8; } .sec-label.teal::before { background:#22d3b8; }
.sec-label.purple { color:#9d79f5; } .sec-label.purple::before { background:#9d79f5; }
.sec-label.amber { color:#BA7517; } .sec-label.amber::before { background:#BA7517; }
.sec-label.green { color:#3B6D11; } .sec-label.green::before { background:#3B6D11; }

.fix-card { background:#0f1117; border:1px solid #1c2030; border-radius:10px; overflow:hidden; margin-bottom:10px; transition:border-color .18s; }
.fix-card:hover { border-color:#252c3d; }
.fix-head { display:flex; align-items:center; justify-content:space-between; padding:10px 16px; background:#12151e; border-bottom:1px solid #1c2030; }
.fix-hl { display:flex; align-items:center; gap:9px; }
.fix-elem { font-family:'JetBrains Mono',monospace; font-size:10px; color:#6b7385; background:#08090d; border:1px solid #1c2030; padding:2px 6px; border-radius:3px; }
.fix-page { font-size:12px; color:#dde1ec; font-weight:500; }
.fix-body { padding:14px 16px; }
.fix-current { font-size:12px; color:#5b8ef5; background:#08090d; border:1px solid #1c2030; border-radius:5px; padding:8px 10px; margin-bottom:8px; line-height:1.55; }
.fix-rec { font-size:13px; color:#3B6D11; background:rgba(59,109,17,.05); border:1px solid rgba(59,109,17,.18); border-radius:5px; padding:8px 10px; margin-bottom:8px; line-height:1.55; font-weight:500; }
.fix-reason { font-size:12px; color:#6b7385; line-height:1.6; }
.bdg { font-family:'JetBrains Mono',monospace; font-size:10px; padding:2px 7px; border-radius:3px; border:1px solid; font-weight:500; }
.p1 { color:#A32D2D; border-color:rgba(162,45,45,.3); background:rgba(162,45,45,.08); }
.p2 { color:#854F0B; border-color:rgba(133,79,11,.3); background:rgba(133,79,11,.08); }
.p3 { color:#3B6D11; border-color:rgba(59,109,17,.3); background:rgba(59,109,17,.08); }

.schema-card { background:#0f1117; border:1px solid #1c2030; border-radius:10px; padding:14px 16px; margin-bottom:10px; }
.sc-type { font-size:13px; font-weight:500; color:#fff; margin-bottom:4px; display:flex; align-items:center; gap:8px; }
.sc-page { font-size:11px; font-family:'JetBrains Mono',monospace; color:#6b7385; margin-bottom:6px; }
.sc-impact { font-size:12px; color:#9d79f5; margin-bottom:8px; line-height:1.5; }
.sc-pri { font-size:10px; font-family:'JetBrains Mono',monospace; padding:2px 7px; border-radius:3px; border:1px solid; }
.sc-pri.critical { color:#A32D2D; border-color:rgba(162,45,45,.3); background:rgba(162,45,45,.08); }
.sc-pri.high { color:#854F0B; border-color:rgba(133,79,11,.3); background:rgba(133,79,11,.08); }
.sc-pri.medium { color:#3B6D11; border-color:rgba(59,109,17,.3); background:rgba(59,109,17,.08); }

.sp-card { background:#0f1117; border:1px solid #1c2030; border-radius:10px; padding:16px 18px; height:100%; }
.sp-tag { font-family:'JetBrains Mono',monospace; font-size:9px; text-transform:uppercase; color:#22d3b8; margin-bottom:8px; letter-spacing:.1em; }
.sp-title { font-size:14px; font-weight:500; color:#fff; margin-bottom:6px; }
.sp-url { font-family:'JetBrains Mono',monospace; font-size:11px; color:#2e3548; margin-bottom:10px; }
.sp-kw { display:flex; gap:5px; flex-wrap:wrap; margin-bottom:10px; }
.sp-kw-pill { font-size:10px; padding:2px 7px; border-radius:3px; background:rgba(91,142,245,.08); border:1px solid rgba(91,142,245,.2); color:#5b8ef5; font-family:'JetBrains Mono',monospace; }
.sp-sections { font-size:12px; color:#6b7385; line-height:1.65; }
.sp-why { font-size:12px; color:#6b7385; border-top:1px solid #1c2030; padding-top:8px; margin-top:8px; line-height:1.55; }

.kw-table-wrap { background:#0f1117; border:1px solid #1c2030; border-radius:10px; overflow:hidden; margin-bottom:16px; }

.faq-e { background:#0f1117; border:1px solid rgba(34,211,184,.18); border-radius:8px; padding:13px 15px; margin-bottom:10px; }
.faq-q { font-size:13px; font-weight:500; color:#fff; margin-bottom:6px; }
.faq-a { font-size:13px; color:#6b7385; line-height:1.7; }
.faq-page { font-size:10px; font-family:'JetBrains Mono',monospace; color:#2e3548; margin-top:5px; }

.crawler-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px; }
.crawler-card { background:#0f1117; border:1px solid #1c2030; border-radius:9px; padding:14px 16px; }
.crawler-name { font-size:12px; font-weight:500; color:#fff; margin-bottom:4px; display:flex; align-items:center; gap:8px; }
.crawler-status { font-size:12px; line-height:1.55; }
.crawler-action { font-size:12px; color:#6b7385; margin-top:6px; border-top:1px solid #1c2030; padding-top:6px; }
.status-pass { color:#34c97e; } .status-fail { color:#ef5050; } .status-warn { color:#f0a500; } .status-unknown { color:#6b7385; }

.roadmap-col { background:#0f1117; border:1px solid #1c2030; border-radius:10px; padding:16px 18px; height:100%; }
.rm-period { font-family:'JetBrains Mono',monospace; font-size:10px; color:#5b8ef5; margin-bottom:5px; }
.rm-theme { font-size:13px; font-weight:500; color:#fff; margin-bottom:10px; }
.rm-item { font-size:12px; color:#6b7385; padding:6px 0; border-bottom:1px solid #1c2030; line-height:1.5; padding-left:12px; position:relative; }
.rm-item:last-child { border-bottom:none; }
.rm-item::before { content:'›'; position:absolute; left:0; color:#2e3548; }

hr { border:none; border-top:1px solid #1c2030; margin:22px 0; }

div[data-testid="stTabs"] > div:first-child > div { background:#08090d !important; border-bottom:1px solid #1c2030 !important; }
div[data-testid="stTabs"] button { font-family:'JetBrains Mono',monospace !important; font-size:11px !important; text-transform:uppercase !important; letter-spacing:.06em !important; color:#6b7385 !important; border-radius:0 !important; padding:10px 18px !important; border:none !important; border-bottom:2px solid transparent !important; background:transparent !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:#fff !important; border-bottom:2px solid #5b8ef5 !important; }

.stTextInput > div > div > input { background:#0f1117 !important; border:1px solid #1c2030 !important; border-radius:8px !important; color:#dde1ec !important; font-family:'JetBrains Mono',monospace !important; font-size:13px !important; }
.stTextInput > div > div > input:focus { border-color:#5b8ef5 !important; }
.stButton > button { background:#5b8ef5 !important; color:#08090d !important; border:none !important; border-radius:8px !important; font-weight:600 !important; font-size:14px !important; padding:10px 28px !important; }
.stButton > button:hover { background:#85b7eb !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="tb-left">
    <div class="tb-title"><span class="tb-dot"></span>SEO Agent</div>
    <div class="tb-sub">Scrape → Analyze → Keyword strategy + schema + supporting pages</div>
  </div>
  <div class="tb-badges">
    <span class="tb-badge blue">ai-seo skill</span>
    <span class="tb-badge teal">schema-markup skill</span>
    <span class="tb-badge purple">programmatic-seo skill</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── API key ───────────────────────────────────────────────────────────────────
api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    with st.sidebar:
        api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")

# ── Pipeline ──────────────────────────────────────────────────────────────────
def pipeline_html(step):
    steps = ["1. Input", "2. Crawl", "3. Prompt", "4. LLM", "5. Results"]
    parts = []
    for i, s in enumerate(steps):
        cls = "done" if i < step else "active" if i == step else ""
        parts.append(f'<div class="ps {cls}">{s}</div>')
        if i < len(steps) - 1:
            parts.append('<div class="pa">›</div>')
    return '<div class="pipe-row">' + "".join(parts) + '</div>'

# ── Inputs ────────────────────────────────────────────────────────────────────
st.markdown(pipeline_html(0), unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    url = st.text_input("Website URL", value="https://cyberpowertools.com", label_visibility="visible")
with col2:
    keyword = st.text_input("Target keyword", value="cyber tools")
with col3:
    st.write("")
    run = st.button("Run SEO Agent →", use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Run ───────────────────────────────────────────────────────────────────────
if run:
    if not api_key:
        st.error("Add your Anthropic API key in the sidebar.")
        st.stop()
    if not url:
        st.error("Enter a URL.")
        st.stop()

    # Step 2: Crawl
    st.markdown(pipeline_html(1), unsafe_allow_html=True)
    with st.spinner("Crawling site pages..."):
        scraped = scrape_seo_site(url)

    pages_ok = len([p for p in scraped.get("pages", {}).values() if p.get("ok")])
    robots = scraped.get("robots", {})
    sitemap = scraped.get("sitemap", {})

    # Schema detection summary
    all_schema = []
    for p in scraped.get("pages", {}).values():
        all_schema.extend(p.get("schema_types", []))
    schema_found = list(set(all_schema))

    st.markdown(f"""
    <div class="scrape-info">
      <div class="s-row"><span class="s-key">Pages crawled</span><span class="s-val">{pages_ok}</span></div>
      <div class="s-row"><span class="s-key">Schema detected</span><span class="s-val {'pass' if schema_found else 'fail'}">{', '.join(schema_found) if schema_found else 'NONE FOUND'}</span></div>
      <div class="s-row"><span class="s-key">Robots.txt</span><span class="s-val {'pass' if robots.get('ok') else 'warn'}">{('accessible' if robots.get('ok') else 'not accessible')}</span></div>
      <div class="s-row"><span class="s-key">Sitemap</span><span class="s-val {'pass' if sitemap.get('ok') else 'warn'}">{(str(sitemap.get('url_count',0)) + ' URLs' if sitemap.get('ok') else 'not found')}</span></div>
      <div class="s-row"><span class="s-key">GPTBot access</span><span class="s-val {'fail' if robots.get('gptbot_blocked') else 'pass'}">{'BLOCKED' if robots.get('gptbot_blocked') else 'allowed' if robots.get('ok') else 'unverified'}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Step 3: Build prompt
    st.markdown(pipeline_html(2), unsafe_allow_html=True)
    formatted = format_seo_for_prompt(scraped, keyword)
    prompt = build_seo_prompt(formatted, keyword, url)

    with st.expander("View generated prompt", expanded=False):
        st.code(prompt[:2000] + "\n\n[...truncated...]", language="text")

    # Step 4: Call LLM
    st.markdown(pipeline_html(3), unsafe_allow_html=True)
    client = anthropic.Anthropic(api_key=api_key)
    result = None

    with st.spinner("Running SEO analysis via Claude API..."):
        try:
            resp = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=SEO_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip().replace("```json", "").replace("```", "").strip()
            result = json.loads(raw)
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.stop()

    # Step 5: Render
    st.markdown(pipeline_html(4), unsafe_allow_html=True)

    audit = result.get("seo_audit", {})
    score = audit.get("overall_score", 0)

    # Score strip
    kw_cluster = result.get("keyword_cluster", [])
    on_page = result.get("on_page_fixes", [])
    schema_plan = result.get("schema_plan", [])
    supporting = result.get("supporting_pages", [])

    st.markdown(f"""
    <div class="score-strip">
      <div class="sc"><div class="sc-n blue-c">{score}/100</div><div class="sc-l">SEO score</div></div>
      <div class="sc"><div class="sc-n amber-c">{len([f for f in on_page if f.get('priority')=='P1'])}</div><div class="sc-l">P1 fixes</div></div>
      <div class="sc"><div class="sc-n teal-c">{len(schema_plan)}</div><div class="sc-l">Schema items</div></div>
      <div class="sc"><div class="sc-n green-c">{len(kw_cluster)}</div><div class="sc-l">Keywords mapped</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Diagnosis
    st.markdown(f"""
    <div class="diag-card">
      <div class="score-ring">{score}</div>
      <div class="diag-meta">
        <div class="dt">SEO diagnosis — {url}</div>
        <div class="dd">{audit.get('score_reasoning','')}</div>
        <div class="de">Estimated time to rank: {audit.get('estimated_time_to_rank','60-90 days with these fixes')}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if audit.get("quick_wins"):
        st.markdown('<div style="font-size:12px;font-weight:500;color:#BA7517;margin-bottom:8px;text-transform:uppercase;letter-spacing:.08em">Quick wins (&lt;1 day)</div>', unsafe_allow_html=True)
        for qw in audit["quick_wins"]:
            st.markdown(f'<div style="font-size:13px;color:#dde1ec;padding:6px 0 6px 14px;border-left:2px solid #BA7517;margin-bottom:6px">{qw}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Tabs
    tabs = st.tabs(["On-Page Fixes", "Schema Plan", "Supporting Pages", "Keyword Cluster", "AI Discoverability", "30/60/90 Roadmap"])

    # Tab 1: On-Page Fixes
    with tabs[0]:
        st.markdown('<div class="sec-label blue">On-page optimizations</div>', unsafe_allow_html=True)
        for fix in on_page:
            pri = fix.get("priority", "P2").lower()
            bdg_cls = {"p1": "p1", "p2": "p2", "p3": "p3"}.get(pri, "p2")
            st.markdown(f"""
            <div class="fix-card">
              <div class="fix-head">
                <div class="fix-hl">
                  <span class="fix-elem">{fix.get('element','')}</span>
                  <span class="fix-page">{fix.get('page','')}</span>
                </div>
                <div style="display:flex;gap:6px">
                  <span class="bdg {bdg_cls}">{fix.get('priority','')}</span>
                  <span class="bdg p3">{fix.get('effort','')} effort</span>
                </div>
              </div>
              <div class="fix-body">
                <div style="font-size:10px;font-family:'JetBrains Mono',monospace;color:#6b7385;margin-bottom:3px">CURRENT</div>
                <div class="fix-current">{fix.get('current','')}</div>
                <div style="font-size:10px;font-family:'JetBrains Mono',monospace;color:#3B6D11;margin-bottom:3px">RECOMMENDED</div>
                <div class="fix-rec">{fix.get('recommended','')}</div>
                <div class="fix-reason">{fix.get('reason','')}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Tab 2: Schema Plan
    with tabs[1]:
        st.markdown('<div class="sec-label purple">Schema markup implementation plan</div>', unsafe_allow_html=True)
        for s in schema_plan:
            pri = s.get("priority", "high")
            st.markdown(f"""
            <div class="schema-card">
              <div class="sc-type">
                {s.get('schema_type','')}
                <span class="sc-pri {pri}">{pri}</span>
              </div>
              <div class="sc-page">Add to: {s.get('page','')}</div>
              <div class="sc-impact">{s.get('ai_impact','')}</div>
            </div>
            """, unsafe_allow_html=True)
            outline = s.get("json_ld_outline", {})
            if outline:
                st.json(outline)

    # Tab 3: Supporting Pages
    with tabs[2]:
        st.markdown('<div class="sec-label teal">Supporting authority pages to create</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, page in enumerate(supporting[:3]):
            with cols[i]:
                kw_pills = "".join(f'<span class="sp-kw-pill">{k}</span>' for k in page.get("target_keywords", [])[:3])
                sections_text = " · ".join(page.get("required_sections", [])[:4])
                st.markdown(f"""
                <div class="sp-card">
                  <div class="sp-tag">Page {i+1} · {page.get('intent','').capitalize()}</div>
                  <div class="sp-title">{page.get('title','')}</div>
                  <div class="sp-url">{page.get('url_slug','')}</div>
                  <div class="sp-kw">{kw_pills}</div>
                  <div class="sp-sections"><strong style="color:#c8cdd8">Required sections:</strong> {sections_text}</div>
                  <div style="font-size:11px;font-family:'JetBrains Mono',monospace;color:#22d3b8;margin-top:8px">{page.get('word_count_target',0):,}+ words</div>
                  <div class="sp-why">{page.get('why_it_builds_authority','')}</div>
                </div>
                """, unsafe_allow_html=True)

    # Tab 4: Keyword Cluster
    with tabs[3]:
        st.markdown('<div class="sec-label blue">Keyword priority cluster</div>', unsafe_allow_html=True)
        import pandas as pd
        if kw_cluster:
            df = pd.DataFrame([{
                "Keyword": k.get("keyword",""),
                "Volume": k.get("monthly_volume",""),
                "Difficulty": k.get("difficulty","").capitalize(),
                "Intent": k.get("intent","").capitalize(),
                "Target Page": k.get("target_page",""),
                "Gap": k.get("current_gap",""),
            } for k in kw_cluster])
            st.dataframe(df, hide_index=True, use_container_width=True)

    # Tab 5: AI Discoverability
    with tabs[4]:
        ai_disc = result.get("ai_discoverability", {})

        st.markdown('<div class="sec-label teal">AI crawler access</div>', unsafe_allow_html=True)
        gpt_status = ai_disc.get("gptbot_access", "unknown")
        bing_status = ai_disc.get("bingbot_access", "unknown")
        gpt_cls = "status-fail" if gpt_status == "blocked" else "status-pass" if gpt_status == "allowed" else "status-unknown"
        bing_cls = "status-fail" if bing_status == "blocked" else "status-pass" if bing_status == "allowed" else "status-unknown"

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="crawler-card">
              <div class="crawler-name">GPTBot (OpenAI)</div>
              <div class="crawler-status {gpt_cls}">Access: {gpt_status.upper()}</div>
              <div class="crawler-action">robots.txt: must have User-agent: GPTBot / Allow: /</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="crawler-card">
              <div class="crawler-name">Bingbot (ChatGPT search)</div>
              <div class="crawler-status {bing_cls}">Access: {bing_status.upper()}</div>
              <div class="crawler-action">{ai_disc.get('bing_webmaster_action','Submit sitemap to Bing Webmaster Tools')}</div>
            </div>
            """, unsafe_allow_html=True)

        if ai_disc.get("content_extractability_gaps"):
            st.markdown('<div class="sec-label teal">Content extractability gaps</div>', unsafe_allow_html=True)
            for gap in ai_disc["content_extractability_gaps"]:
                st.markdown(f'<div style="font-size:13px;color:#dde1ec;padding:6px 0 6px 14px;border-left:2px solid #ef5050;margin-bottom:6px">{gap}</div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-label teal">FAQ citation engine — DryQ ready entries</div>', unsafe_allow_html=True)
        for faq in ai_disc.get("faq_citation_entries", []):
            st.markdown(f"""
            <div class="faq-e">
              <div class="faq-q">{faq.get('question','')}</div>
              <div class="faq-a">{faq.get('answer','')}</div>
              <div class="faq-page">Add to: {faq.get('page_to_add_to','')}</div>
            </div>
            """, unsafe_allow_html=True)

    # Tab 6: Roadmap
    with tabs[5]:
        roadmap = result.get("thirty_sixty_ninety", {})
        st.markdown('<div class="sec-label blue">Implementation roadmap</div>', unsafe_allow_html=True)
        r_cols = st.columns(3)
        for col, (key, label) in zip(r_cols, [("day_30","30 Days"), ("day_60","60 Days"), ("day_90","90 Days")]):
            period = roadmap.get(key, {})
            items_html = "".join(f'<div class="rm-item">{a}</div>' for a in period.get("actions", []))
            with col:
                st.markdown(f"""
                <div class="roadmap-col">
                  <div class="rm-period">{label}</div>
                  <div class="rm-theme">{period.get('theme','')}</div>
                  {items_html}
                </div>
                """, unsafe_allow_html=True)

    with st.expander("Raw JSON output", expanded=False):
        st.json(result)
