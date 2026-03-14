import streamlit as st
import anthropic
import json
import re
import os
from cro_scraper import scrape_landing_page, format_for_prompt
from cro_prompts import CRO_SYSTEM_PROMPT, build_cro_prompt, build_copy_deep_dive_prompt

st.set_page_config(
    page_title="CRO Agent — SRI Labs",
    page_icon="⚡",
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
.tb-title { font-size:15px; font-weight:700; color:#fff; display:flex; align-items:center; gap:10px; }
.tb-dot { width:8px; height:8px; border-radius:50%; background:#22d3b8; box-shadow:0 0 8px #22d3b8; animation:pulse 2.4s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.2} }
.tb-sub { font-size:12px; color:#6b7385; margin-top:2px; }
.tb-badge { font-family:'JetBrains Mono',monospace; font-size:10px; color:#22d3b8; background:rgba(34,211,184,.07); border:1px solid rgba(34,211,184,.18); padding:4px 11px; border-radius:5px; }

.pipeline-row { display:flex; align-items:center; gap:0; margin-bottom:28px; }
.pipe-step { display:flex; align-items:center; gap:8px; padding:8px 14px; background:#0f1117; border:1px solid #1c2030; font-size:12px; color:#6b7385; }
.pipe-step:first-child { border-radius:7px 0 0 7px; }
.pipe-step:last-child { border-radius:0 7px 7px 0; }
.pipe-step.active { background:#0f1117; border-color:#22d3b8; color:#22d3b8; }
.pipe-step.done { background:rgba(52,201,126,.08); border-color:rgba(52,201,126,.25); color:#34c97e; }
.pipe-arrow { color:#2e3548; font-size:14px; background:#08090d; border-top:1px solid #1c2030; border-bottom:1px solid #1c2030; padding:8px 4px; }
.pipe-num { font-family:'JetBrains Mono',monospace; font-size:10px; opacity:.6; }

.grade-card { background:#0f1117; border:1px solid #1c2030; border-radius:12px; padding:20px 24px; margin-bottom:20px; display:flex; gap:20px; align-items:flex-start; }
.grade-ring { width:64px; height:64px; border-radius:50%; border:3px solid; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:700; flex-shrink:0; }
.grade-A { border-color:#34c97e; color:#34c97e; }
.grade-B { border-color:#22d3b8; color:#22d3b8; }
.grade-C { border-color:#f0a500; color:#f0a500; }
.grade-D { border-color:#ef5050; color:#ef5050; }
.grade-F { border-color:#ef5050; color:#ef5050; }
.grade-meta { flex:1; }
.grade-title { font-size:14px; font-weight:600; color:#fff; margin-bottom:6px; }
.grade-text { font-size:13px; color:#6b7385; line-height:1.65; }

.tcard { background:#0f1117; border:1px solid #1c2030; border-radius:11px; overflow:hidden; margin-bottom:12px; }
.tcard-head { display:flex; align-items:center; justify-content:space-between; padding:11px 18px; background:#12151e; border-bottom:1px solid #1c2030; }
.tcard-hl { display:flex; align-items:center; gap:10px; }
.tcard-id { font-family:'JetBrains Mono',monospace; font-size:10px; color:#6b7385; background:#08090d; border:1px solid #1c2030; padding:2px 7px; border-radius:3px; }
.tcard-name { font-size:13px; font-weight:600; color:#fff; }
.tcard-body { padding:16px 18px; }
.t-desc { font-size:13px; color:#6b7385; line-height:1.65; margin-bottom:12px; }

.cv-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px; }
.cv-box { background:#08090d; border:1px solid #1c2030; border-radius:7px; padding:12px 14px; }
.cv-lbl { font-family:'JetBrains Mono',monospace; font-size:9px; text-transform:uppercase; letter-spacing:.1em; margin-bottom:7px; }
.cv-lbl.ctrl { color:#5b8ef5; }
.cv-lbl.test { color:#34c97e; }
.cv-text { font-size:12px; color:#dde1ec; line-height:1.5; }

.bdg { font-family:'JetBrains Mono',monospace; font-size:10px; padding:2px 8px; border-radius:4px; border:1px solid; font-weight:500; }
.bdg-p1 { color:#ef5050; border-color:rgba(239,80,80,.3); background:rgba(239,80,80,.08); }
.bdg-p2 { color:#f0a500; border-color:rgba(240,165,0,.3); background:rgba(240,165,0,.08); }
.bdg-p3 { color:#34c97e; border-color:rgba(52,201,126,.3); background:rgba(52,201,126,.08); }
.bdg-copy { color:#5b8ef5; border-color:rgba(91,142,245,.3); background:rgba(91,142,245,.08); }

.hyp { font-family:'JetBrains Mono',monospace; font-size:11px; color:#22d3b8; background:rgba(34,211,184,.04); border:1px solid rgba(34,211,184,.14); border-radius:6px; padding:10px 12px; margin-top:10px; line-height:1.6; }

.issue-row { display:flex; gap:10px; align-items:flex-start; padding:9px 0; border-bottom:1px solid #1c2030; font-size:13px; }
.issue-row:last-child { border-bottom:none; }
.idot { width:7px; height:7px; border-radius:50%; flex-shrink:0; margin-top:5px; }
.idot.critical { background:#ef5050; }
.idot.warning { background:#f0a500; }
.idot.minor { background:#22d3b8; }
.ilbl { color:#dde1ec; flex:1; line-height:1.45; }
.ifix { font-size:11px; color:#6b7385; margin-top:2px; }

.ev-card { background:#08090d; border:1px solid #1c2030; border-radius:7px; padding:11px 13px; }
.ev-name { font-family:'JetBrains Mono',monospace; font-size:11px; color:#22d3b8; margin-bottom:4px; }
.ev-desc { font-size:12px; color:#6b7385; line-height:1.5; }

.coh-card { background:#08090d; border:1px solid #1c2030; border-radius:7px; padding:12px 14px; }
.coh-name { font-size:12px; font-weight:600; color:#fff; margin-bottom:5px; }
.coh-def { font-size:11px; color:#22d3b8; margin-bottom:5px; font-family:'JetBrains Mono',monospace; }
.coh-ad { font-size:12px; color:#6b7385; }

.copy-card { background:#0f1117; border:1px solid #1c2030; border-radius:10px; padding:16px 18px; margin-bottom:10px; }
.copy-elem { font-family:'JetBrains Mono',monospace; font-size:10px; text-transform:uppercase; color:#6b7385; margin-bottom:10px; letter-spacing:.08em; }
.copy-current { font-size:12px; color:#5b8ef5; background:#08090d; border:1px solid #1c2030; border-radius:6px; padding:10px 12px; margin-bottom:8px; line-height:1.6; }
.copy-new { font-size:13px; color:#34c97e; background:rgba(52,201,126,.04); border:1px solid rgba(52,201,126,.18); border-radius:6px; padding:10px 12px; margin-bottom:8px; line-height:1.6; }
.copy-why { font-size:12px; color:#6b7385; line-height:1.6; }

.hero-var { background:#0f1117; border:1px solid #1c2030; border-radius:10px; padding:18px 20px; margin-bottom:12px; }
.hv-name { font-family:'JetBrains Mono',monospace; font-size:10px; text-transform:uppercase; color:#9d79f5; margin-bottom:12px; letter-spacing:.08em; }
.hv-hl { font-size:16px; font-weight:600; color:#fff; margin-bottom:7px; line-height:1.3; }
.hv-sub { font-size:13px; color:#c8cdd8; margin-bottom:7px; line-height:1.6; }
.hv-body { font-size:13px; color:#6b7385; margin-bottom:10px; line-height:1.65; }
.hv-cta { display:inline-block; font-size:12px; font-weight:600; padding:8px 18px; border-radius:6px; background:rgba(34,211,184,.1); border:1px solid rgba(34,211,184,.3); color:#22d3b8; margin-bottom:10px; }
.hv-why { font-size:12px; color:#6b7385; border-top:1px solid #1c2030; padding-top:9px; margin-top:6px; line-height:1.55; }

.scrape-info { background:#0f1117; border:1px solid #1c2030; border-radius:9px; padding:14px 16px; margin-bottom:20px; }
.scrape-row { display:flex; justify-content:space-between; font-size:12px; padding:4px 0; border-bottom:1px solid #1c2030; }
.scrape-row:last-child { border-bottom:none; }
.scrape-key { color:#6b7385; }
.scrape-val { color:#dde1ec; font-family:'JetBrains Mono',monospace; font-size:11px; }

.pills { display:flex; gap:6px; flex-wrap:wrap; margin-top:8px; }
.pill { font-size:11px; padding:3px 8px; border-radius:4px; background:#12151e; border:1px solid #1c2030; color:#6b7385; }

hr { border:none; border-top:1px solid #1c2030; margin:22px 0; }

div[data-testid="stTabs"] > div:first-child > div { background:#08090d !important; border-bottom:1px solid #1c2030 !important; }
div[data-testid="stTabs"] button { font-family:'JetBrains Mono',monospace !important; font-size:11px !important; text-transform:uppercase !important; letter-spacing:.06em !important; color:#6b7385 !important; border-radius:0 !important; padding:10px 18px !important; border:none !important; border-bottom:2px solid transparent !important; background:transparent !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:#fff !important; border-bottom:2px solid #22d3b8 !important; }

.stTextInput > div > div > input { background:#0f1117 !important; border:1px solid #1c2030 !important; border-radius:8px !important; color:#dde1ec !important; font-family:'JetBrains Mono',monospace !important; font-size:13px !important; }
.stTextInput > div > div > input:focus { border-color:#22d3b8 !important; }
.stTextArea > div > div > textarea { background:#0f1117 !important; border:1px solid #1c2030 !important; color:#dde1ec !important; font-size:13px !important; }
.stSelectbox > div > div { background:#0f1117 !important; border:1px solid #1c2030 !important; color:#dde1ec !important; }
.stButton > button { background:#22d3b8 !important; color:#08090d !important; border:none !important; border-radius:8px !important; font-weight:600 !important; font-size:14px !important; padding:10px 28px !important; }
.stButton > button:hover { background:#5dcaa5 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div>
    <div class="tb-title"><span class="tb-dot"></span>CRO Agent</div>
    <div class="tb-sub">Scrape → Analyze → Test recommendations</div>
  </div>
  <div class="tb-badge">page-cro skill</div>
</div>
""", unsafe_allow_html=True)

# ── API Key ───────────────────────────────────────────────────────────────────
api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    with st.sidebar:
        api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")

# ── Pipeline indicator ────────────────────────────────────────────────────────
def pipeline_html(step):
    steps = ["1. Input", "2. Scrape", "3. Prompt", "4. LLM", "5. Results"]
    parts = []
    for i, s in enumerate(steps):
        if i < step:
            cls = "done"
        elif i == step:
            cls = "active"
        else:
            cls = ""
        parts.append(f'<div class="pipe-step {cls}">{s}</div>')
        if i < len(steps) - 1:
            parts.append('<div class="pipe-arrow">›</div>')
    return '<div class="pipeline-row">' + "".join(parts) + '</div>'

# ── Input form ────────────────────────────────────────────────────────────────
st.markdown(pipeline_html(0), unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    url = st.text_input("Landing page URL", value="https://srilabs.com/pages/sri-dryq-fb-prelander", label_visibility="visible")
with col2:
    st.write("")
    run = st.button("Run CRO Agent →", use_container_width=True)

c1, c2, c3 = st.columns(3)
with c1:
    traffic_source = st.selectbox("Traffic source", ["Meta Ads (Facebook/Instagram)", "Google Ads", "TikTok Ads", "Email", "Organic"], index=0)
with c2:
    audience = st.text_input("Target audience", value="Women 35–65")
with c3:
    goal = st.text_input("Conversion goal", value="Purchase DryQ hair dryer")

video_context = st.text_area(
    "Video context (optional — describe any key video on the page so the agent understands it)",
    value="Hero video: FOX 5 Localist SD host Ashley Jacobs endorses DryQ red light therapy for hair growth. Segment is ~3 min. Earned media / news feature. This is the primary trust-builder on the page.",
    height=80,
)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Run ───────────────────────────────────────────────────────────────────────
if run:
    if not api_key:
        st.error("Add your Anthropic API key in the sidebar.")
        st.stop()
    if not url:
        st.error("Enter a URL.")
        st.stop()

    # Step 2: Scrape
    st.markdown(pipeline_html(1), unsafe_allow_html=True)
    with st.spinner("Scraping page..."):
        scraped = scrape_landing_page(url)

    if not scraped.get("ok"):
        st.error(f"Could not scrape the page: {scraped.get('error')}")
        st.stop()

    # Show scrape summary
    st.markdown(f"""
    <div class="scrape-info">
      <div class="scrape-row"><span class="scrape-key">URL scraped</span><span class="scrape-val">{scraped['url']}</span></div>
      <div class="scrape-row"><span class="scrape-key">Headings found</span><span class="scrape-val">{len(scraped['headings'])}</span></div>
      <div class="scrape-row"><span class="scrape-key">CTA buttons detected</span><span class="scrape-val">{len(scraped['ctas'])}</span></div>
      <div class="scrape-row"><span class="scrape-key">Social proof signals</span><span class="scrape-val">{len(scraped['social_proof'])}</span></div>
      <div class="scrape-row"><span class="scrape-key">Videos detected</span><span class="scrape-val">{len(scraped['videos_detected'])}</span></div>
      <div class="scrape-row"><span class="scrape-key">Body copy length</span><span class="scrape-val">{len(scraped['body_text'])} chars</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Step 3: Build prompts
    st.markdown(pipeline_html(2), unsafe_allow_html=True)
    formatted = format_for_prompt(scraped)
    cro_prompt = build_cro_prompt(formatted, traffic_source, audience, goal, video_context)
    copy_prompt = build_copy_deep_dive_prompt(formatted, audience, goal)

    with st.expander("View generated prompt (CRO analysis)", expanded=False):
        st.code(cro_prompt[:2000] + "\n\n[...truncated for display...]", language="text")

    # Step 4: Call LLM
    st.markdown(pipeline_html(3), unsafe_allow_html=True)
    client = anthropic.Anthropic(api_key=api_key)

    cro_result = None
    copy_result = None

    with st.spinner("Running CRO analysis via Claude API..."):
        try:
            resp = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8192,
                system=CRO_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": cro_prompt}],
            )
            raw = resp.content[0].text.strip()
            # Strip code fences
            raw = re.sub(r'^```[a-z]*\n?', '', raw, flags=re.MULTILINE)
            raw = raw.replace('```', '').strip()
            # Find the outermost JSON object
            start = raw.find('{')
            end = raw.rfind('}') + 1
            if start != -1 and end > start:
                raw = raw[start:end]
            # Replace smart quotes with straight quotes
            raw = raw.replace('\u2018', "'").replace('\u2019', "'")
            raw = raw.replace('\u201c', '"').replace('\u201d', '"')
            cro_result = json.loads(raw)
        except Exception as e:
            st.error(f"CRO analysis failed: {e}")

    with st.spinner("Running copy deep-dive via Claude API..."):
        try:
            resp2 = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8192,
                system=CRO_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": copy_prompt}],
            )
            raw2 = resp2.content[0].text.strip()
            raw2 = re.sub(r'^```[a-z]*\n?', '', raw2, flags=re.MULTILINE)
            raw2 = raw2.replace('```', '').strip()
            start2 = raw2.find('{')
            end2 = raw2.rfind('}') + 1
            if start2 != -1 and end2 > start2:
                raw2 = raw2[start2:end2]
            raw2 = raw2.replace('\u2018', "'").replace('\u2019', "'")
            raw2 = raw2.replace('\u201c', '"').replace('\u201d', '"')
            copy_result = json.loads(raw2)
        except Exception as e:
            st.warning(f"Copy deep-dive failed: {e}")

    # Step 5: Render results
    st.markdown(pipeline_html(4), unsafe_allow_html=True)

    if not cro_result:
        st.error("No results to display.")
        st.stop()

    diag = cro_result.get("page_diagnosis", {})
    grade = diag.get("overall_grade", "?")

    # ── Page diagnosis ──
    st.markdown(f"""
    <div class="grade-card">
      <div class="grade-ring grade-{grade}">{grade}</div>
      <div class="grade-meta">
        <div class="grade-title">Page diagnosis — {url}</div>
        <div class="grade-text">{diag.get('grade_reasoning', '')}</div>
        <div style="margin-top:10px;font-size:12px;color:#ef5050"><strong>Primary conversion leak:</strong> {diag.get('primary_conversion_leak', '')}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if diag.get("quick_wins"):
        st.markdown('<div style="font-size:12px;font-weight:600;color:#f0a500;margin-bottom:8px;text-transform:uppercase;letter-spacing:.08em">Quick wins (&lt;1 day)</div>', unsafe_allow_html=True)
        for qw in diag["quick_wins"]:
            st.markdown(f'<div style="font-size:13px;color:#dde1ec;padding:6px 0 6px 14px;border-left:2px solid #f0a500;margin-bottom:6px">{qw}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Tabs for results ──
    tabs = st.tabs(["CRO Tests", "Copy Rewrites", "Copy Variants", "Tracking Plan", "Structural Issues"])

    # Tab 1: CRO Tests
    with tabs[0]:
        tests = cro_result.get("cro_tests", [])
        for test in tests:
            pri = test.get("priority", "P2").lower()
            bdg_cls = {"p1": "bdg-p1", "p2": "bdg-p2", "p3": "bdg-p3"}.get(pri, "bdg-p2")
            ttype = test.get("type", "")
            type_cls = "bdg-copy" if ttype == "copy" else "bdg-p2"
            st.markdown(f"""
            <div class="tcard">
              <div class="tcard-head">
                <div class="tcard-hl">
                  <span class="tcard-id">{test.get('id','')}</span>
                  <span class="tcard-name">{test.get('name','')}</span>
                </div>
                <div style="display:flex;gap:6px">
                  <span class="bdg {bdg_cls}">{test.get('priority','')}</span>
                  <span class="bdg {type_cls}">{ttype}</span>
                </div>
              </div>
              <div class="tcard-body">
                <div class="cv-grid">
                  <div class="cv-box"><div class="cv-lbl ctrl">Control</div><div class="cv-text">{test.get('control','')}</div></div>
                  <div class="cv-box"><div class="cv-lbl test">Variant</div><div class="cv-text">{test.get('variant','')}</div></div>
                </div>
                <div class="hyp">{test.get('hypothesis','')}</div>
                <div class="pills">
                  <span class="pill">Primary: {test.get('primary_metric','')}</span>
                  <span class="pill">Expected: {test.get('expected_lift','')}</span>
                  <span class="pill">Effort: {test.get('effort','')}</span>
                </div>
                <div style="font-size:12px;color:#6b7385;margin-top:10px;line-height:1.55"><strong style="color:#c8cdd8">Audience insight:</strong> {test.get('audience_insight','')}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Tab 2: Copy Rewrites
    with tabs[1]:
        rewrites = cro_result.get("copywriting_rewrites", [])
        for rw in rewrites:
            st.markdown(f"""
            <div class="copy-card">
              <div class="copy-elem">{rw.get('element','')}</div>
              <div style="font-size:10px;color:#6b7385;margin-bottom:4px;font-family:'JetBrains Mono',monospace">CURRENT</div>
              <div class="copy-current">{rw.get('current_copy','')}</div>
              <div style="font-size:10px;color:#34c97e;margin-bottom:4px;font-family:'JetBrains Mono',monospace">REWRITE</div>
              <div class="copy-new">{rw.get('rewritten_copy','')}</div>
              <div class="copy-why"><strong style="color:#c8cdd8">Why it converts better:</strong> {rw.get('rationale','')}</div>
            </div>
            """, unsafe_allow_html=True)

    # Tab 3: Copy Variants (from deep dive)
    with tabs[2]:
        if copy_result:
            audit = copy_result.get("copy_audit", {})
            if audit:
                st.markdown(f"""
                <div style="background:#0f1117;border:1px solid rgba(157,121,245,.2);border-radius:10px;padding:16px 18px;margin-bottom:20px">
                  <div style="font-size:13px;font-weight:600;color:#9d79f5;margin-bottom:8px">Copy audit</div>
                  <div style="font-size:13px;color:#6b7385;line-height:1.65"><strong style="color:#dde1ec">Biggest problem:</strong> {audit.get('biggest_copy_problem','')}</div>
                  <div style="font-size:13px;color:#6b7385;line-height:1.65;margin-top:6px"><strong style="color:#dde1ec">Missing emotional hook:</strong> {audit.get('emotional_hook_missing','')}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div style="font-size:12px;font-weight:600;color:#9d79f5;margin-bottom:14px;text-transform:uppercase;letter-spacing:.08em">Three hero variants — A/B test ready</div>', unsafe_allow_html=True)
            for var in copy_result.get("hero_variants", []):
                st.markdown(f"""
                <div class="hero-var">
                  <div class="hv-name">{var.get('variant_name','')}</div>
                  <div class="hv-hl">{var.get('headline','')}</div>
                  <div class="hv-sub">{var.get('subheadline','')}</div>
                  <div class="hv-body">{var.get('body_copy','')}</div>
                  <div class="hv-cta">{var.get('cta','')}</div>
                  <div class="hv-why"><strong>Why it works:</strong> {var.get('why_it_works','')}</div>
                </div>
                """, unsafe_allow_html=True)

            offer_vars = copy_result.get("offer_framing_variants", [])
            if offer_vars:
                st.markdown('<hr><div style="font-size:12px;font-weight:600;color:#9d79f5;margin-bottom:12px;text-transform:uppercase;letter-spacing:.08em">Offer framing variants</div>', unsafe_allow_html=True)
                for ov in offer_vars:
                    st.markdown(f"""
                    <div style="background:#0f1117;border:1px solid #1c2030;border-radius:9px;padding:14px 16px;margin-bottom:10px">
                      <div style="font-size:12px;font-weight:600;color:#f0a500;margin-bottom:6px">{ov.get('variant','')}</div>
                      <div style="font-size:13px;color:#34c97e;margin-bottom:6px">{ov.get('copy','')}</div>
                      <div style="font-size:12px;color:#6b7385">{ov.get('psychology','')}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Copy deep-dive analysis unavailable.")

    # Tab 4: Tracking Plan
    with tabs[3]:
        tracking = cro_result.get("tracking_plan", {})
        video_events   = tracking.get("video_events", [])
        cta_events     = tracking.get("cta_events", [])
        scroll_events  = tracking.get("scroll_events", [])
        eng_events     = tracking.get("engagement_events", [])
        cohorts        = tracking.get("retargeting_cohorts", [])

        def render_section_label(label, color="#22d3b8"):
            st.markdown(f'''<div style="font-size:10px;font-weight:500;text-transform:uppercase;letter-spacing:.1em;color:{color};margin:18px 0 10px;display:flex;align-items:center;gap:8px"><span style="width:14px;height:1px;background:{color};display:block"></span>{label}</div>''', unsafe_allow_html=True)

        def render_ev_grid(events, show_retarget=False):
            cols = st.columns(2)
            for i, ev in enumerate(events):
                with cols[i % 2]:
                    retarget_badge = ""
                    if show_retarget and ev.get("retarget_value"):
                        rv = ev["retarget_value"]
                        rv_color = {"high": "#34c97e", "medium": "#f0a500", "low": "#6b7385"}.get(rv, "#6b7385")
                        retarget_badge = f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:{rv_color};margin-top:4px">retarget: {rv}</div>'
                    st.markdown(f"""
                    <div class="ev-card" style="margin-bottom:10px">
                      <div class="ev-name">{ev.get("event_name","")}</div>
                      <div class="ev-desc"><strong style="color:#c8cdd8">Trigger:</strong> {ev.get("trigger","")}</div>
                      <div class="ev-desc" style="margin-top:4px">{ev.get("purpose","")}</div>
                      <div style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:#2e3548;margin-top:4px">{ev.get("platform","")}</div>
                      {retarget_badge}
                    </div>
                    """, unsafe_allow_html=True)

        # Video events
        if video_events:
            render_section_label("Video events", "#9d79f5")
            render_ev_grid(video_events, show_retarget=True)

        # CTA events
        if cta_events:
            render_section_label("CTA & purchase intent events", "#f0a500")
            render_ev_grid(cta_events)

        # Scroll events — table layout
        if scroll_events:
            render_section_label("Scroll depth events", "#5b8ef5")
            cols = st.columns(4)
            for i, ev in enumerate(scroll_events[:4]):
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="ev-card" style="margin-bottom:10px;text-align:center">
                      <div style="font-size:20px;font-weight:500;color:#5b8ef5;line-height:1">{ev.get("depth","")}%</div>
                      <div style="font-size:10px;font-family:\'JetBrains Mono\',monospace;color:#22d3b8;margin:4px 0">{ev.get("event_name","")}</div>
                      <div class="ev-desc">{ev.get("landmark","")}</div>
                      <div class="ev-desc" style="margin-top:4px;font-style:italic">{ev.get("purpose","")}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # Engagement events
        if eng_events:
            render_section_label("Engagement signals", "#22d3b8")
            render_ev_grid(eng_events)

        # Retargeting cohorts
        render_section_label("Retargeting cohorts", "#34c97e")
        tier_colors = {"1": "#34c97e", "2": "#f0a500", "3": "#5b8ef5", "exclude": "#ef5050"}
        coh_cols = st.columns(len(cohorts) if cohorts else 4)
        for i, coh in enumerate(cohorts[:4]):
            tier = str(coh.get("tier", ""))
            tc = tier_colors.get(tier, "#6b7385")
            with coh_cols[i]:
                st.markdown(f"""
                <div class="coh-card">
                  <div style="font-size:10px;font-family:\'JetBrains Mono\',monospace;color:{tc};margin-bottom:5px;text-transform:uppercase">{"Tier " + tier if tier != "exclude" else "Exclude"}</div>
                  <div class="coh-name">{coh.get("cohort_name","")}</div>
                  <div class="coh-def">{coh.get("definition","")}</div>
                  <div class="coh-ad" style="margin-top:5px">{coh.get("recommended_ad","")}</div>
                  <div style="font-size:10px;font-family:\'JetBrains Mono\',monospace;color:#2e3548;margin-top:5px">{coh.get("bid_modifier","")}</div>
                </div>
                """, unsafe_allow_html=True)

    # Tab 5: Structural Issues
    with tabs[4]:
        issues = cro_result.get("structural_issues", [])
        st.markdown('<div style="background:#0f1117;border:1px solid #1c2030;border-radius:10px;padding:4px 16px">', unsafe_allow_html=True)
        for issue in issues:
            sev = issue.get("severity", "warning")
            st.markdown(f"""
            <div class="issue-row">
              <span class="idot {sev}"></span>
              <div>
                <div class="ilbl">{issue.get('issue','')}</div>
                <div class="ifix">Fix: {issue.get('fix','')}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Raw JSON expander
    with st.expander("Raw JSON output", expanded=False):
        st.json(cro_result)
