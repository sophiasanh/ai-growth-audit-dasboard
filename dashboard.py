import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Growth Audit — SRI Labs & Cyber Power Tools",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #08090d !important; color: #dde1ec; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── sidebar off ── */
section[data-testid="stSidebar"] { display: none; }

/* ── top bar ── */
.topbar {
    background: rgba(8,9,13,.95); backdrop-filter: blur(20px);
    border-bottom: 1px solid #1c2030;
    padding: 14px 32px; display: flex; align-items: center;
    justify-content: space-between; position: sticky; top:0; z-index:999;
}
.tb-brand { display:flex; align-items:center; gap:10px; }
.tb-dot { width:8px; height:8px; border-radius:50%; background:#22d3b8;
    box-shadow:0 0 8px #22d3b8; animation: pulse 2.4s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.25;transform:scale(.7)} }
.tb-title { font-size:14px; font-weight:700; color:#fff; letter-spacing:-.2px; }
.tb-sub   { font-size:11px; color:#6b7385; margin-top:2px; }
.tb-tag   { font-family:'JetBrains Mono',monospace; font-size:10px; color:#22d3b8;
    background:rgba(34,211,184,.07); border:1px solid rgba(34,211,184,.2);
    padding:4px 11px; border-radius:5px; }

/* ── inner page ── */
.inner { padding: 32px 36px 64px; max-width: 1140px; margin: 0 auto; }

/* ── score bar ── */
.score-strip { display:flex; gap:14px; margin-bottom:32px; flex-wrap:wrap; }
.score-card {
    flex:1; min-width:130px; background:#0f1117; border:1px solid #1c2030;
    border-radius:10px; padding:16px 18px;
}
.sc-num { font-size:30px; font-weight:700; line-height:1; margin-bottom:4px; }
.sc-lbl { font-size:10px; color:#6b7385; text-transform:uppercase; letter-spacing:.08em; }
.amber { color:#f0a500; } .teal  { color:#22d3b8; }
.blue  { color:#5b8ef5; } .purple{ color:#9d79f5; }
.green { color:#34c97e; } .red   { color:#ef5050;  }

/* ── section eyebrow ── */
.eyebrow {
    font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:500;
    letter-spacing:.14em; text-transform:uppercase;
    display:flex; align-items:center; gap:9px; margin-bottom:12px;
}
.eyebrow::before { content:''; width:16px; height:1px; display:block; }
.eyebrow.amber { color:#f0a500; } .eyebrow.amber::before { background:#f0a500; }
.eyebrow.blue  { color:#5b8ef5; } .eyebrow.blue::before  { background:#5b8ef5; }
.eyebrow.teal  { color:#22d3b8; } .eyebrow.teal::before  { background:#22d3b8; }
.eyebrow.purple{ color:#9d79f5; } .eyebrow.purple::before{ background:#9d79f5; }

/* ── section title ── */
.sec-title { font-size:22px; font-weight:700; color:#fff; margin-bottom:6px; line-height:1.2; }
.sec-sub   { font-size:13px; color:#6b7385; line-height:1.7; margin-bottom:28px; }
.sec-sub strong { color:#c8cdd8; }

/* ── context strip ── */
.ctx-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
    gap:10px; margin-bottom:28px; }
.ctx-item { background:#0f1117; border:1px solid #1c2030; border-radius:8px; padding:12px 14px; }
.ctx-lbl  { font-size:9px; font-weight:600; text-transform:uppercase; letter-spacing:.1em;
    color:#2e3548; margin-bottom:4px; }
.ctx-val  { font-size:13px; color:#dde1ec; font-weight:500; }
.ctx-val.hi { color:#f0a500; }

/* ── test card ── */
.tcard {
    background:#0f1117; border:1px solid #1c2030; border-radius:12px;
    overflow:hidden; margin-bottom:14px; transition:border-color .18s;
}
.tcard:hover { border-color:#252c3d; }
.tcard-head {
    display:flex; align-items:center; justify-content:space-between;
    padding:12px 20px; background:#12151e; border-bottom:1px solid #1c2030;
}
.tcard-hl { display:flex; align-items:center; gap:10px; }
.tcard-num {
    font-family:'JetBrains Mono',monospace; font-size:10px; color:#6b7385;
    background:#08090d; border:1px solid #1c2030; padding:2px 7px; border-radius:3px;
}
.tcard-title { font-size:14px; font-weight:600; color:#fff; }
.tcard-body  { padding:18px 20px; }
.tcard-body .desc { font-size:13px; color:#6b7385; line-height:1.7; margin-bottom:14px; }

/* ── badge ── */
.bdg { font-family:'JetBrains Mono',monospace; font-size:10px; padding:3px 9px;
    border-radius:4px; border:1px solid; font-weight:500; white-space:nowrap; }
.bdg-copy   { color:#5b8ef5; border-color:rgba(91,142,245,.28); background:rgba(91,142,245,.08); }
.bdg-p1     { color:#ef5050; border-color:rgba(239,80,80,.28); background:rgba(239,80,80,.08); }
.bdg-p2     { color:#f0a500; border-color:rgba(240,165,0,.28); background:rgba(240,165,0,.08); }
.bdg-track  { color:#22d3b8; border-color:rgba(34,211,184,.28); background:rgba(34,211,184,.08); }
.bdg-purple { color:#9d79f5; border-color:rgba(157,121,245,.28); background:rgba(157,121,245,.08); }
.bdg-green  { color:#34c97e; border-color:rgba(52,201,126,.28); background:rgba(52,201,126,.08); }

/* ── copy compare ── */
.cc-table { background:#08090d; border:1px solid #1c2030; border-radius:8px;
    overflow:hidden; margin-bottom:14px; }
.cc-hdr { display:flex; justify-content:space-between; padding:8px 12px;
    background:#12151e; border-bottom:1px solid #1c2030;
    font-family:'JetBrains Mono',monospace; font-size:10px; color:#6b7385; }
.cc-row { display:grid; grid-template-columns:110px 1fr 1fr;
    border-bottom:1px solid #1c2030; font-size:13px; }
.cc-row:last-child { border-bottom:none; }
.cc-cell { padding:9px 12px; }
.cc-lbl  { font-family:'JetBrains Mono',monospace; font-size:9px; text-transform:uppercase;
    color:#6b7385; background:#12151e; border-right:1px solid #1c2030; }
.cc-ctrl { color:#5b8ef5; }
.cc-test { color:#34c97e; }

/* ── hypothesis ── */
.hyp {
    font-family:'JetBrains Mono',monospace; font-size:11px; line-height:1.65;
    color:#22d3b8; background:rgba(34,211,184,.04);
    border:1px solid rgba(34,211,184,.14); border-radius:6px;
    padding:11px 13px; margin-top:12px;
}

/* ── metric pills ── */
.mpills { display:flex; gap:7px; flex-wrap:wrap; margin-top:10px; }
.mpill  { font-size:11px; padding:3px 9px; border-radius:4px;
    background:rgba(91,142,245,.07); border:1px solid rgba(91,142,245,.18); color:#5b8ef5; }

/* ── variant box ── */
.vbox { background:#08090d; border:1px solid #1c2030; border-radius:8px; padding:13px 15px; }
.vbox-lbl { font-family:'JetBrains Mono',monospace; font-size:9px; text-transform:uppercase;
    letter-spacing:.1em; margin-bottom:7px; }
.vbox-lbl.ctrl { color:#5b8ef5; }
.vbox-lbl.test { color:#34c97e; }
.vbox-body { font-size:13px; color:#dde1ec; line-height:1.5; }
.vbox-body em { font-style:normal; color:#f0a500; font-weight:600; }

/* ── pros/cons ── */
.pros-card { background:#08090d; border:1px solid rgba(52,201,126,.2);
    border-radius:9px; padding:16px 18px; }
.cons-card { background:#08090d; border:1px solid rgba(240,165,0,.18);
    border-radius:9px; padding:16px 18px; }
.pc-title { font-size:13px; font-weight:700; margin-bottom:10px;
    display:flex; align-items:center; gap:7px; }
.pc-item  { display:flex; align-items:center; gap:9px; font-size:13px;
    padding:5px 0; border-bottom:1px solid #1c2030; }
.pc-item:last-child { border-bottom:none; }

/* ── who-for grid ── */
.who-grid { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:14px; }
.who-item { display:flex; align-items:center; gap:10px; padding:10px 13px;
    background:#08090d; border:1px solid #1c2030; border-radius:7px;
    font-size:13px; color:#dde1ec; }

/* ── audit row ── */
.arow { display:flex; align-items:flex-start; gap:10px; padding:9px 0;
    border-bottom:1px solid #1c2030; font-size:13px; }
.arow:last-child { border-bottom:none; }
.adot { width:7px; height:7px; border-radius:50%; flex-shrink:0; margin-top:5px; }
.adot.pass { background:#34c97e; }
.adot.fail { background:#ef5050; }
.adot.warn { background:#f0a500; }
.albl  { color:#dde1ec; flex:1; line-height:1.45; }
.adet  { font-size:11px; color:#6b7385; margin-top:2px; }

/* ── faq entry ── */
.faq-e { background:#08090d; border:1px solid rgba(34,211,184,.18);
    border-radius:8px; padding:14px 16px; margin-bottom:10px; }
.faq-q { font-size:13px; font-weight:600; color:#fff; margin-bottom:6px; }
.faq-a { font-size:13px; color:#6b7385; line-height:1.7; }

/* ── action item ── */
.act { background:#0f1117; border:1px solid #1c2030; border-radius:9px;
    padding:14px 16px; margin-bottom:10px; display:flex; gap:12px; }
.act-num {
    font-family:'JetBrains Mono',monospace; font-size:11px; color:#f0a500;
    background:rgba(240,165,0,.07); border:1px solid rgba(240,165,0,.18);
    width:26px; height:26px; border-radius:5px; display:flex;
    align-items:center; justify-content:center; flex-shrink:0;
}
.act-title { font-size:13px; font-weight:600; color:#fff; margin-bottom:4px; }
.act-body  { font-size:12px; color:#6b7385; line-height:1.65; }
.act-code  { background:#08090d; border:1px solid #1c2030; border-radius:5px;
    padding:10px 12px; font-family:'JetBrains Mono',monospace; font-size:11px;
    color:#dde1ec; margin-top:9px; line-height:1.8; overflow-x:auto; }
.act-code .kw { color:#22d3b8; }
.act-code .vl { color:#f0a500; }
.act-code .cm { color:#2e3548; }

/* ── supporting pages ── */
.sp-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-top:12px; }
.sp-card { background:#08090d; border:1px solid #1c2030; border-radius:7px; padding:14px 16px; }
.sp-tag  { font-family:'JetBrains Mono',monospace; font-size:9px; text-transform:uppercase;
    color:#22d3b8; margin-bottom:8px; letter-spacing:.1em; }
.sp-title { font-size:13px; font-weight:600; color:#fff; margin-bottom:6px; }
.sp-body  { font-size:12px; color:#6b7385; line-height:1.55; }
.sp-url   { font-family:'JetBrains Mono',monospace; font-size:10px; color:#2e3548; margin-top:8px; }

/* ── cohort cards ── */
.coh-grid { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:10px; }
.coh-card { padding:10px 12px; background:#08090d; border-radius:7px;
    font-size:12px; font-weight:500; border:1px solid; }

/* ── divider ── */
.divider { border:none; border-top:1px solid #1c2030; margin:28px 0; }

/* ── dataframe override ── */
div[data-testid="stDataFrame"] { background: #0f1117 !important; border-radius:10px; border:1px solid #1c2030; }

/* ── tab styles ── */
div[data-testid="stTabs"] > div:first-child > div {
    background: #08090d !important;
    border-bottom: 1px solid #1c2030 !important;
    gap: 4px !important;
    padding: 0 0 0 0 !important;
}
div[data-testid="stTabs"] button {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: .06em !important;
    color: #6b7385 !important;
    border-radius: 0 !important;
    padding: 10px 18px !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #fff !important;
    border-bottom: 2px solid #22d3b8 !important;
}
div[data-testid="stTabContent"] { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─── TOP BAR ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="tb-brand">
    <span class="tb-dot"></span>
    <div>
      <div class="tb-title">AI Growth Audit Dashboard</div>
      <div class="tb-sub">SRI Labs &nbsp;·&nbsp; Cyber Power Tools</div>
    </div>
  </div>
  <div class="tb-tag">marketingskills agent pack</div>
</div>
""", unsafe_allow_html=True)


# ─── INNER WRAPPER ────────────────────────────────────────────────────────────
st.markdown('<div class="inner">', unsafe_allow_html=True)

# ─── SCORE STRIP ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="score-strip">
  <div class="score-card"><div class="sc-num amber">5</div><div class="sc-lbl">CRO Tests · Prelander</div></div>
  <div class="score-card"><div class="sc-num amber">4</div><div class="sc-lbl">PDP Conversion Tests</div></div>
  <div class="score-card"><div class="sc-num blue">5</div><div class="sc-lbl">SEO Actions · Cyber Tools</div></div>
  <div class="score-card"><div class="sc-num purple">5</div><div class="sc-lbl">AEO / GEO Improvements</div></div>
  <div class="score-card"><div class="sc-num green">4</div><div class="sc-lbl">FAQ Citations Built</div></div>
  <div class="score-card"><div class="sc-num teal">6</div><div class="sc-lbl">Schema Types Missing</div></div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
t1, t2, t3, t4 = st.tabs([
    "① CRO — SRI Labs",
    "② PDP — DryQ",
    "③ SEO — Cyber Tools",
    "④ AI Discoverability",
])


# ══════════════════════════════════════════════
# TAB 1 — CRO
# ══════════════════════════════════════════════
with t1:
    st.markdown('<div style="padding-top:28px">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow amber">CRO Optimization · SRI Labs FB Prelander</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Conversion Rate Tests</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Agent: <strong>page-cro · ab-test-setup · copywriting · analytics-tracking</strong>. The hero video is the primary persuasion asset. Every test is designed around maximizing video engagement and converting the 35–65 female Meta audience into buyers.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("""
        <div class="ctx-grid">
          <div class="ctx-item"><div class="ctx-lbl">Primary Goal</div><div class="ctx-val hi">DryQ Purchase</div></div>
          <div class="ctx-item"><div class="ctx-lbl">Traffic</div><div class="ctx-val">Meta Ads · UGC</div></div>
          <div class="ctx-item"><div class="ctx-lbl">Audience</div><div class="ctx-val">Women 35–65</div></div>
          <div class="ctx-item"><div class="ctx-lbl">Price</div><div class="ctx-val">$224.99 (–$75)</div></div>
          <div class="ctx-item"><div class="ctx-lbl">Reviews</div><div class="ctx-val">4.5★ · 1,079</div></div>
          <div class="ctx-item"><div class="ctx-lbl">Sales</div><div class="ctx-val">100K+ sold</div></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="tcard" style="border-left:3px solid rgba(240,165,0,.4);margin-top:0">
          <div class="tcard-body">
            <div style="font-size:11px;font-family:'JetBrains Mono',monospace;color:#f0a500;margin-bottom:8px">🎬 VIDEO IS THE PRIMARY PERSUASION ASSET</div>
            <div style="font-size:13px;color:#6b7385;line-height:1.65">The FOX 5 / Ashley Jacobs red light therapy segment is the single most important conversion element on this page. All five tests are built around maximizing video engagement and using completion as a purchase intent signal.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── TEST 1: Video Tracking ──
    st.markdown("""
    <div class="tcard">
      <div class="tcard-head">
        <div class="tcard-hl"><span class="tcard-num">Test 1</span><span class="tcard-title">Video Interaction Tracking</span></div>
        <span class="bdg bdg-track">Analytics · Foundation</span>
      </div>
      <div class="tcard-body">
        <p class="desc">Video engagement is not currently a conversion signal. There is no way to know how many users watch, how far they get, or how video completion correlates with purchase. This test builds the behavioral data layer every other test depends on.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px">
          <span style="font-family:'JetBrains Mono',monospace;font-size:11px;padding:5px 12px;border-radius:5px;background:rgba(34,211,184,.07);border:1px solid rgba(34,211,184,.18);color:#22d3b8">video_start</span>
          <span style="font-family:'JetBrains Mono',monospace;font-size:11px;padding:5px 12px;border-radius:5px;background:rgba(34,211,184,.07);border:1px solid rgba(34,211,184,.18);color:#22d3b8">video_25%</span>
          <span style="font-family:'JetBrains Mono',monospace;font-size:11px;padding:5px 12px;border-radius:5px;background:rgba(34,211,184,.07);border:1px solid rgba(34,211,184,.18);color:#22d3b8">video_50%</span>
          <span style="font-family:'JetBrains Mono',monospace;font-size:11px;padding:5px 12px;border-radius:5px;background:rgba(34,211,184,.07);border:1px solid rgba(34,211,184,.18);color:#22d3b8">video_complete</span>
          <span style="font-family:'JetBrains Mono',monospace;font-size:11px;padding:5px 12px;border-radius:5px;background:rgba(240,165,0,.07);border:1px solid rgba(240,165,0,.18);color:#f0a500">→ retarget 50%+ viewers</span>
        </div>
        <div class="hyp">💡 Expected: Higher purchase intent segmentation. Users who watch 50%+ are significantly more likely to convert — retargeting this segment with a direct purchase ad closes the loop from the prelander visit.</div>
        <div class="mpills">
          <span class="mpill">video_start rate</span>
          <span class="mpill">video_50% rate</span>
          <span class="mpill">video_complete → ATC rate</span>
          <span class="mpill">retarget ROAS vs. cold</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TEST 2: UGC Copy ──
    st.markdown("""
    <div class="tcard">
      <div class="tcard-head">
        <div class="tcard-hl"><span class="tcard-num">Test 2</span><span class="tcard-title">UGC Audience Copy Variant</span></div>
        <span class="bdg bdg-copy">Copy Test · Priority 1</span>
      </div>
      <div class="tcard-body">
        <p class="desc">Current copy is product-centric and tech-heavy. Cold Meta traffic arriving from UGC ads expects copy that mirrors their identity and experience — not a spec sheet.</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px">
          <div class="vbox">
            <div class="vbox-lbl ctrl">Control</div>
            <div class="vbox-body">"Join thousands of women elevating their hairstyling routine"</div>
          </div>
          <div class="vbox">
            <div class="vbox-lbl test">Variant — Audience-First</div>
            <div class="vbox-body">Headline: <em>"Thousands of Women Over 40 Are Switching to the DryQ"</em><br><br>Sub: "The infrared hair dryer designed to support thicker, healthier-looking hair while cutting drying time in half."</div>
          </div>
        </div>
        <div class="hyp">💡 Expected: Better resonance with the 35–65 female audience. Social proof framing ("thousands of women over 40") reduces skepticism, speaks to their identity, and positions DryQ as the proven choice among their peers.</div>
        <div class="mpills">
          <span class="mpill">Primary: add-to-cart rate</span>
          <span class="mpill">Secondary: time on page</span>
          <span class="mpill">2,000+ per variant · 14 days</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TEST 3: Social Proof ──
    st.markdown("""
    <div class="tcard">
      <div class="tcard-head">
        <div class="tcard-hl"><span class="tcard-num">Test 3</span><span class="tcard-title">Social Proof Placement — Above Fold</span></div>
        <span class="bdg bdg-p1">Priority 1</span>
      </div>
      <div class="tcard-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px">
          <div class="vbox">
            <div class="vbox-lbl ctrl">Control — Current Position</div>
            <div class="vbox-body">"Over 100,000 Sold" appears mid-page, below the fold, after the video section. Users must scroll to find it.</div>
          </div>
          <div class="vbox">
            <div class="vbox-lbl test">Variant — Move Above Fold</div>
            <div class="vbox-body">"Over 100,000 Sold" and the 4.5★ review count placed <em>directly above the CTA button</em>, visible on page load on mobile.</div>
          </div>
        </div>
        <div class="hyp">💡 Meta traffic requires instant trust signals. Users arriving from a UGC ad are in decision mode — not discovery mode. Social proof at the point of decision has the highest conversion leverage on cold traffic.</div>
        <div class="mpills">
          <span class="mpill">Primary: CTA click rate above fold</span>
          <span class="mpill">Secondary: scroll depth</span>
          <span class="mpill">Heatmap: click distribution</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TEST 4: CTA ──
    st.markdown("""
    <div class="tcard">
      <div class="tcard-head">
        <div class="tcard-hl"><span class="tcard-num">Test 4</span><span class="tcard-title">CTA Copy — Three Variants</span></div>
        <span class="bdg bdg-copy">Copy Test · Priority 1</span>
      </div>
      <div class="tcard-body">
        <p class="desc">Current CTA: "Upgrade to the DryQ" — passive and product-named. Test three alternatives: transactional, benefit-led, and identity-oriented.</p>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px">
          <div style="text-align:center;padding:14px;background:#08090d;border:1px solid #1c2030;border-radius:8px">
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#6b7385;text-transform:uppercase;margin-bottom:10px">Variant A</div>
            <div style="display:inline-block;font-size:12px;font-weight:600;padding:8px 16px;border-radius:6px;background:rgba(240,165,0,.1);border:1px solid rgba(240,165,0,.3);color:#f0a500">Shop DryQ</div>
            <div style="font-size:11px;color:#6b7385;margin-top:10px">Transactional. Simple.</div>
          </div>
          <div style="text-align:center;padding:14px;background:#08090d;border:2px solid rgba(34,211,184,.3);border-radius:8px">
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#22d3b8;text-transform:uppercase;margin-bottom:10px">Variant B ★ Recommended</div>
            <div style="display:inline-block;font-size:12px;font-weight:600;padding:8px 16px;border-radius:6px;background:rgba(34,211,184,.1);border:1px solid rgba(34,211,184,.3);color:#22d3b8">Start Your Healthier Hair Routine</div>
            <div style="font-size:11px;color:#6b7385;margin-top:10px">Benefit + identity. Sells the outcome.</div>
          </div>
          <div style="text-align:center;padding:14px;background:#08090d;border:1px solid #1c2030;border-radius:8px">
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#6b7385;text-transform:uppercase;margin-bottom:10px">Variant C</div>
            <div style="display:inline-block;font-size:12px;font-weight:600;padding:8px 16px;border-radius:6px;background:rgba(91,142,245,.1);border:1px solid rgba(91,142,245,.3);color:#5b8ef5">Get the DryQ Dryer</div>
            <div style="font-size:11px;color:#6b7385;margin-top:10px">Product-specific. Brand recall.</div>
          </div>
        </div>
        <div class="hyp">💡 Hypothesis: Variant B outperforms — it sells the transformation, not the transaction. Women 35–65 are buying a result ("healthier hair routine"), not a device.</div>
        <div class="mpills">
          <span class="mpill">Measure: CTR per variant</span>
          <span class="mpill">Measure: add-to-cart rate</span>
          <span class="mpill">Duration: 14 days minimum</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TEST 5: Full Copy Rewrite (Required) ──
    st.markdown("""
    <div class="tcard" style="border-color:rgba(91,142,245,.3)">
      <div class="tcard-head" style="background:rgba(91,142,245,.06);border-bottom-color:rgba(91,142,245,.2)">
        <div class="tcard-hl"><span class="tcard-num">Test 5</span><span class="tcard-title">Hero Section Full Copywriting Rewrite</span></div>
        <span class="bdg bdg-copy">🎯 Required Copy Test</span>
      </div>
      <div class="tcard-body">
        <p class="desc">The current hero is tech-heavy — it leads with infrared specs, ionic technology, and nanometer wavelengths. The 35–65 female audience arriving from a UGC ad doesn't come to a landing page to read a spec sheet. They come to feel understood and see themselves in the outcome.</p>
        <div class="cc-table">
          <div class="cc-hdr"><span>Full hero section rewrite — copy only, no layout changes</span><span>Control vs. Variant</span></div>
          <div class="cc-row" style="background:#12151e">
            <div class="cc-cell cc-lbl">Element</div>
            <div class="cc-cell" style="color:#5b8ef5;font-family:'JetBrains Mono',monospace;font-size:9px;text-transform:uppercase">Control (Current)</div>
            <div class="cc-cell" style="color:#34c97e;font-family:'JetBrains Mono',monospace;font-size:9px;text-transform:uppercase">Test Variant</div>
          </div>
          <div class="cc-row">
            <div class="cc-cell cc-lbl">H1</div>
            <div class="cc-cell cc-ctrl">"Say goodbye to frizz with the advanced SRI DryQ"</div>
            <div class="cc-cell cc-test">"Dry Faster. Healthier Hair."</div>
          </div>
          <div class="cc-row">
            <div class="cc-cell cc-lbl">Subhead</div>
            <div class="cc-cell cc-ctrl">"Join thousands of women elevating their hairstyling routine"</div>
            <div class="cc-cell cc-test">"The SRI DryQ uses infrared light therapy and ionic airflow to reduce frizz and support stronger-looking hair."</div>
          </div>
          <div class="cc-row">
            <div class="cc-cell cc-lbl">Social proof</div>
            <div class="cc-cell cc-ctrl">Tech feature bullets — ions, nanometers, wavelengths</div>
            <div class="cc-cell cc-test">"Trusted by stylists and loved by thousands of women upgrading their hair routine."</div>
          </div>
          <div class="cc-row">
            <div class="cc-cell cc-lbl">CTA</div>
            <div class="cc-cell cc-ctrl">"Upgrade to the DryQ"</div>
            <div class="cc-cell cc-test">"Start Your Healthier Hair Routine"</div>
          </div>
        </div>
        <div class="hyp">💡 Hypothesis: The simplified, outcome-led variant ("Dry Faster. Healthier Hair.") outperforms the tech-heavy control because it leads with the result, backs it with social proof from real women, and matches the register of the UGC creative that drove the click. Expected lift: 15–25% ATC rate on mobile.</div>
        <div class="mpills">
          <span class="mpill">Primary: add-to-cart rate</span>
          <span class="mpill">Secondary: video_start rate</span>
          <span class="mpill">Secondary: scroll depth to CTA</span>
          <span class="mpill">Duration: 14–21 days · 2,000+ / variant</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 — PDP
# ══════════════════════════════════════════════
with t2:
    st.markdown('<div style="padding-top:28px">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow amber">PDP Optimization · SRI DryQ Product Page</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Product Page Conversion Tests</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Agent: <strong>page-cro · copywriting · analytics-tracking</strong>. All traffic — regardless of source — lands here. These four tests add content layers that convert undecided buyers and build behavioral cohorts for retargeting. <strong>Primary goal: Purchase.</strong></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="ctx-grid">
      <div class="ctx-item"><div class="ctx-lbl">URL</div><div class="ctx-val" style="font-family:'JetBrains Mono',monospace;font-size:11px">srilabs.com/products/sri-dryq</div></div>
      <div class="ctx-item"><div class="ctx-lbl">Goal</div><div class="ctx-val hi">Purchase</div></div>
      <div class="ctx-item"><div class="ctx-lbl">Universal Destination</div><div class="ctx-val hi">All traffic ends here</div></div>
      <div class="ctx-item"><div class="ctx-lbl">Offer</div><div class="ctx-val">$70 off · Free shipping</div></div>
      <div class="ctx-item"><div class="ctx-lbl">Mobile Traffic</div><div class="ctx-val hi">~85%</div></div>
      <div class="ctx-item"><div class="ctx-lbl">Reviews</div><div class="ctx-val">4.5★ · 1,079 verified</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Test 1 — Who This Is For
    st.markdown("""
    <div class="tcard">
      <div class="tcard-head">
        <div class="tcard-hl"><span class="tcard-num">Test 1</span><span class="tcard-title">"Who DryQ Is Perfect For" Section</span></div>
        <span class="bdg bdg-copy">Copy Test · Priority 1</span>
      </div>
      <div class="tcard-body">
        <p class="desc">The DryQ PDP lists features but never explicitly tells the visitor whether this product is right for them. For a $224 purchase, buyers need to see themselves in the product before committing. This is the most important unasked question on any PDP: <em style="color:#c8cdd8">"Is this for someone like me?"</em></p>
        <div class="who-grid">
          <div class="who-item"><span style="color:#34c97e;font-size:15px">✓</span> Women experiencing thinning hair</div>
          <div class="who-item"><span style="color:#34c97e;font-size:15px">✓</span> Anyone wanting faster drying time</div>
          <div class="who-item"><span style="color:#34c97e;font-size:15px">✓</span> People struggling with frizz</div>
          <div class="who-item"><span style="color:#34c97e;font-size:15px">✓</span> Anyone upgrading from traditional dryers</div>
        </div>
        <div class="hyp">💡 Hypothesis: Buyers who see themselves named in a "Who This Is For" section experience higher purchase confidence. Expected: 8–14% ATC lift for users who scroll to the section.</div>
        <div class="mpills">
          <span class="mpill">Primary: ATC rate post-section</span>
          <span class="mpill">Secondary: scroll depth to section</span>
          <span class="mpill">Heatmap: engagement with cards</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Test 2 — Pros & Cons
    st.markdown("""
    <div class="tcard">
      <div class="tcard-head">
        <div class="tcard-hl"><span class="tcard-num">Test 2</span><span class="tcard-title">Pros & Considerations Section</span></div>
        <span class="bdg bdg-p1">Priority 1</span>
      </div>
      <div class="tcard-body">
        <p class="desc">The PDP only presents positive attributes. Women 35–65 making a $224 decision distrust one-sided pages. Transparent "Considerations" alongside pros builds credibility, preempts post-purchase regret, and signals the brand has nothing to hide. Also a top AI citation format for purchase-intent queries.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    p_col, c_col = st.columns(2)
    with p_col:
        st.markdown("""
        <div class="pros-card">
          <div class="pc-title" style="color:#34c97e">✓ &nbsp;Pros</div>
          <div class="pc-item"><span style="color:#34c97e;font-size:13px">→</span><span style="font-size:13px;color:#dde1ec">Fast drying — cuts drying time significantly</span></div>
          <div class="pc-item"><span style="color:#34c97e;font-size:13px">→</span><span style="font-size:13px;color:#dde1ec">Infrared red light therapy for hair health</span></div>
          <div class="pc-item"><span style="color:#34c97e;font-size:13px">→</span><span style="font-size:13px;color:#dde1ec">Lightweight at 11.8 oz — easy to hold</span></div>
          <div class="pc-item"><span style="color:#34c97e;font-size:13px">→</span><span style="font-size:13px;color:#dde1ec">Foldable design — travel-friendly</span></div>
          <div class="pc-item"><span style="color:#34c97e;font-size:13px">→</span><span style="font-size:13px;color:#dde1ec">99-day money-back guarantee</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c_col:
        st.markdown("""
        <div class="cons-card">
          <div class="pc-title" style="color:#f0a500">◎ &nbsp;Considerations</div>
          <div class="pc-item"><span style="color:#f0a500;font-size:13px">→</span><span style="font-size:13px;color:#6b7385">Premium price point — an investment in hair health</span></div>
          <div class="pc-item"><span style="color:#f0a500;font-size:13px">→</span><span style="font-size:13px;color:#6b7385">Best results achieved with diffuser attachment</span></div>
          <div style="font-size:11px;color:#2e3548;margin-top:12px;line-height:1.55">"Considerations" framing — not "Cons" — builds trust without negativity. Pairing the premium price with the 99-day guarantee reframes cost as a safe investment.</div>
        </div>
        """, unsafe_allow_html=True)

    # Test 3 — Comparison Table
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tcard">
      <div class="tcard-head">
        <div class="tcard-hl"><span class="tcard-num">Test 3</span><span class="tcard-title">DryQ vs. Standard Dryer — Comparison Table</span></div>
        <span class="bdg bdg-p1">Priority 1</span>
      </div>
      <div class="tcard-body">
        <p class="desc">A side-by-side comparison keeps the buying decision on your PDP rather than a competitor's. Frames DryQ against the familiar baseline (a standard dryer), making the technology advantages visually undeniable. Structured tables are also a top AI citation format — AI quotes specific cells verbatim.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    comp_df = pd.DataFrame({
        "Feature": ["Dry time", "Frizz reduction", "Infrared therapy", "Negative ions", "Hair damage risk", "Weight", "Guarantee"],
        "✅ SRI DryQ": ["Fast", "High", "Yes — 650nm", "Yes", "Low — gentle heat", "11.8 oz", "99 days"],
        "Standard Dryer": ["Medium", "Low", "No", "No", "Medium–High", "Varies", "Rarely"],
    })
    st.dataframe(comp_df, hide_index=True, use_container_width=True)
    st.markdown("""<div class="hyp" style="margin-top:10px">💡 Hypothesis: Comparison table anchors DryQ's advantages against the familiar baseline — making tech differentiators visually undeniable rather than requiring buyers to read and interpret spec copy. AI models also cite specific table cells when answering product comparison queries.</div>""", unsafe_allow_html=True)

    # Test 4 — Heatmap
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tcard">
      <div class="tcard-head">
        <div class="tcard-hl"><span class="tcard-num">Test 4</span><span class="tcard-title">Video & Behavioral Heatmap Tracking</span></div>
        <span class="bdg bdg-track">Analytics · Conversion Cohorts</span>
      </div>
      <div class="tcard-body">
        <p class="desc">No behavioral data layer currently exists on the PDP. Without knowing where users drop off and how video completion correlates with purchase, every optimization is a guess. This test instruments the page to build conversion cohorts — audiences segmented by real engagement — enabling precision retargeting.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    coh1, coh2, coh3, coh4 = st.columns(4)
    with coh1:
        st.markdown("""<div style="padding:12px;background:#08090d;border:1px solid rgba(34,211,184,.25);border-radius:8px;font-size:12px;color:#22d3b8;font-weight:600;text-align:center">🎯 High Intent<br><span style="font-size:11px;font-weight:400;color:#6b7385">video_complete<br>+ no purchase<br>→ retarget</span></div>""", unsafe_allow_html=True)
    with coh2:
        st.markdown("""<div style="padding:12px;background:#08090d;border:1px solid rgba(240,165,0,.25);border-radius:8px;font-size:12px;color:#f0a500;font-weight:600;text-align:center">📍 Mid Intent<br><span style="font-size:11px;font-weight:400;color:#6b7385">scroll 75%<br>+ no ATC<br>→ retarget</span></div>""", unsafe_allow_html=True)
    with coh3:
        st.markdown("""<div style="padding:12px;background:#08090d;border:1px solid rgba(239,80,80,.2);border-radius:8px;font-size:12px;color:#ef5050;font-weight:600;text-align:center">🚫 Low Intent<br><span style="font-size:11px;font-weight:400;color:#6b7385">scroll &lt;25%<br>→ exclude<br>from spend</span></div>""", unsafe_allow_html=True)
    with coh4:
        st.markdown("""<div style="padding:12px;background:#08090d;border:1px solid rgba(52,201,126,.25);border-radius:8px;font-size:12px;color:#34c97e;font-weight:600;text-align:center">✅ Purchasers<br><span style="font-size:11px;font-weight:400;color:#6b7385">→ seed<br>lookalike<br>audience</span></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="hyp" style="margin-top:12px">💡 Expected: Cohorts built from real behavioral data are 3–5× more likely to convert than generic cold traffic. This layer also reveals which PDP content drives the most conversion lift — prioritizing every future test.</div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 — SEO
# ══════════════════════════════════════════════
with t3:
    st.markdown('<div style="padding-top:28px">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow blue">SEO Optimization · Cyber Power Tools</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Keyword Strategy: "cyber tools"</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Agent: <strong>ai-seo · schema-markup · programmatic-seo</strong>. The brand name and @cybertools social handles already signal the right entity — these five on-page fixes close the gap to page-1 ranking in 60–90 days.</div>', unsafe_allow_html=True)

    a_col, b_col = st.columns(2)
    with a_col:
        st.markdown('<div style="font-size:12px;font-weight:600;color:#5b8ef5;margin-bottom:10px">📋 Current Baseline</div>', unsafe_allow_html=True)
        for status, label, detail in [
            ("fail", "Title tag is generic", "Current: 'Cyber Power Tools' — no keyword targeting"),
            ("fail", "H1 doesn't contain 'cyber tools'", "Misses exact keyword match"),
            ("fail", "No keyword context paragraph", "Zero body copy for crawlers to parse"),
            ("fail", "No topical authority pages", "No guides, comparisons, or pillar content"),
            ("fail", "No schema markup detected", "Missing Organization, Product, BreadcrumbList"),
            ("pass", "@cybertools on 4 social platforms", "Entity co-occurrence signal in place"),
        ]:
            st.markdown(f"""<div class="arow"><span class="adot {status}"></span><div><div class="albl">{label}</div><div class="adet">{detail}</div></div></div>""", unsafe_allow_html=True)

    with b_col:
        st.markdown('<div style="font-size:12px;font-weight:600;color:#5b8ef5;margin-bottom:10px">🎯 Keyword Opportunity</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(240,165,0,.06);border:1px solid rgba(240,165,0,.18);border-radius:8px;padding:12px 14px;margin-bottom:12px;font-size:13px;color:#6b7385;line-height:1.65">
          <strong style="color:#f0a500">"Cyber tools"</strong> is low-competition with high brand alignment.<br>Page-1 achievable in 60–90 days with these fixes.
        </div>
        """, unsafe_allow_html=True)
        for status, label, detail in [
            ("pass", "Brand name contains exact keyword", "Cyber Power Tools = cyber + tools"),
            ("pass", "4 social platforms all @cybertools", "Entity co-occurrence: FB, IG, X, YouTube"),
            ("fail", "No blog or content hub", "Zero topical authority articles"),
            ("fail", "No backlinks from tool review sites", "Missing hardware/tools publication citations"),
        ]:
            st.markdown(f"""<div class="arow"><span class="adot {status}"></span><div><div class="albl">{label}</div><div class="adet">{detail}</div></div></div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:14px">SEO Action Plan</div>', unsafe_allow_html=True)

    seo_actions = [
        ("01", "Title Tag Rewrite",
         'Current: <span style="color:#6b7385;font-style:italic">"Cyber Power Tools"</span><br>Test: <span style="color:#34c97e;font-weight:600">"Cyber Tools | Professional Power Tools by Cyber Power Tools"</span>',
         None),
        ("02", "H1 — Keyword-Forward Headline",
         'Current: "Cyber Power Tools" → Replace: <span style="color:#34c97e;font-weight:600">"Cyber Tools Built for Professionals"</span><br>Puts the exact keyword in the most important on-page signal.',
         None),
        ("03", "Add Keyword Context Paragraph Under Hero",
         None,
         '"Cyber Power Tools designs high-performance cyber tools engineered for durability, precision, and professional use. Our cyber tools lineup includes advanced drills, saws, and job-site equipment trusted by contractors worldwide."'),
        ("04", "Create Three Supporting Authority Pages",
         "AI and Google reward topical depth. These three pages build the content cluster needed to rank the homepage for 'cyber tools' as a category term — not just a brand name.",
         None),
        ("05", "Add Organization Schema with alternateName: 'Cyber Tools'",
         "The alternateName field maps the brand to the keyword. No schema currently detected — this is the fastest trust signal for both Google and AI crawlers.",
         '{ "@type": "Organization", "name": "Cyber Power Tools", "alternateName": "Cyber Tools", "sameAs": ["https://x.com/cybertools"] }'),
    ]

    for num, title, body, code in seo_actions:
        code_html = f'<div class="act-code"><span class="vl">{code}</span></div>' if code else ""
        body_html = f'<div class="act-body">{body}</div>' if body else ""
        st.markdown(f"""
        <div class="act">
          <div class="act-num">{num}</div>
          <div style="flex:1">
            <div class="act-title">{title}</div>
            {body_html}
            {code_html}
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Supporting pages
    st.markdown("""
    <div class="sp-grid">
      <div class="sp-card">
        <div class="sp-tag">Page 1</div>
        <div class="sp-title">Best Cyber Tools for Contractors</div>
        <div class="sp-body">Targets commercial buying intent. Showcases the full lineup with contractor use-case context.</div>
        <div class="sp-url">/blogs/best-cyber-tools-contractors</div>
      </div>
      <div class="sp-card">
        <div class="sp-tag">Page 2</div>
        <div class="sp-title">Cyber Tools vs Traditional Power Tools</div>
        <div class="sp-body">High-intent comparison content. AI platforms cite comparison pages for "which is better" queries.</div>
        <div class="sp-url">/blogs/cyber-tools-vs-traditional</div>
      </div>
      <div class="sp-card">
        <div class="sp-tag">Page 3 — Pillar</div>
        <div class="sp-title">Complete Guide to Cyber Tools</div>
        <div class="sp-body">Topical authority hub. Links all PDPs and sub-pages. The page Google uses to understand the brand category.</div>
        <div class="sp-url">/blogs/complete-guide-cyber-tools</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:12px">Keyword Priority Cluster</div>', unsafe_allow_html=True)
    kw_df = pd.DataFrame({
        "Keyword": ["cyber tools","cyber power tools","best cyber tools for contractors",
                    "cyber tools vs traditional","complete guide to cyber tools",
                    "best tactical flashlight","cordless angle grinder 20v"],
        "Intent": ["Commercial","Brand","Commercial","Informational","Informational","Commercial","Commercial"],
        "Est. Volume": ["8,100/mo","2,400/mo","1,800/mo","900/mo","600/mo","22,000/mo","5,400/mo"],
        "Difficulty": ["Medium","Low","Low","Low","Low","High","Medium"],
        "Priority": ["HIGH","HIGH","HIGH","HIGH","HIGH","MED","MED"],
        "Target Page": ["Homepage","Homepage","Supporting p.1","Supporting p.2","Pillar page","Flashlight PDP","Grinder PDP"],
    })
    st.dataframe(kw_df, hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — AEO / GEO
# ══════════════════════════════════════════════
with t4:
    st.markdown('<div style="padding-top:28px">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow purple">AI Discoverability Audit · AEO / GEO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">SRI Labs — AI Readiness</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Agent: <strong>ai-seo · schema-markup</strong>. The core shift: AI platforms synthesize answers rather than returning link lists. Brands must optimize to be <em>quoted as the answer</em> — not just rank for keywords.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(34,211,184,.05),rgba(157,121,245,.05));border:1px solid rgba(34,211,184,.16);border-radius:10px;padding:18px 22px;margin-bottom:28px">
      <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:7px">SEO → AEO: The Core Change</div>
      <div style="font-size:13px;color:#6b7385;line-height:1.7">Traditional SEO: rank #1 on Google. &nbsp;<strong style="color:#fff">→</strong>&nbsp; AEO/GEO: become the <em>cited answer inside</em> the AI response. ChatGPT, Perplexity, and Google AI Overviews synthesize answers from trusted sources. If your content isn't structured for extraction, AI skips it and quotes a competitor instead.<br><span style="color:#2e3548;font-size:12px;margin-top:6px;display:block">AI search drives &lt;1% of traffic today but converts 6–23× better — users arrive at the final decision stage.</span></div>
    </div>
    """, unsafe_allow_html=True)

    # 5 audit areas
    areas = [
        ("1 — AI Readability", "purple"),
        ("2 — Schema Verification", "purple"),
        ("3 — Product Page Extractability", "purple"),
        ("4 — Robots.txt AI Crawlers", "purple"),
        ("5 — FAQ Citation Engine", "purple"),
    ]

    # Area 1
    st.markdown('<div class="eyebrow purple">1 — AI Readability Check</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1:
        st.markdown('<div style="font-size:12px;font-weight:600;color:#9d79f5;margin-bottom:8px">Paragraph & Heading Audit</div>', unsafe_allow_html=True)
        for s, l, d in [
            ("fail","Paragraphs exceed 4 sentences","AI skips dense text — split into short blocks or bullets"),
            ("fail","No H2/H3 hierarchy in product sections","Missing headings = low citation probability"),
            ("fail","Features in prose, not bullets","Bullets are directly quotable; prose requires re-synthesis"),
            ("fail","No 'Key Points' summary box","3–4 bullet summary at top doubles AI citation frequency"),
            ("pass","Core content in raw HTML","Visible without JS — AI crawlers can read it directly"),
        ]:
            st.markdown(f"""<div class="arow"><span class="adot {s}"></span><div><div class="albl">{l}</div><div class="adet">{d}</div></div></div>""", unsafe_allow_html=True)
    with r2:
        st.markdown('<div style="font-size:12px;font-weight:600;color:#9d79f5;margin-bottom:8px">Readability Rules</div>', unsafe_allow_html=True)
        for term, rule in [
            ("Paragraphs","Max 3–4 sentences. If a human can skim it, AI can summarize it."),
            ("Headings","H1 → H2 → H3 hierarchy on every page. Directs AI to specific answers."),
            ("Bullet lists","Make facts explicit and directly quotable. Don't bury data in paragraphs."),
            ("Key Points","3–4 bullets at the top trains AI on exactly what to extract from the page."),
        ]:
            st.markdown(f"""<div style="display:flex;gap:10px;align-items:flex-start;font-size:13px;padding:8px 10px;background:#08090d;border:1px solid #1c2030;border-radius:6px;margin-bottom:6px"><span style="color:#22d3b8;flex-shrink:0">→</span><span style="color:#6b7385"><strong style="color:#dde1ec">{term}:</strong> {rule}</span></div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Area 2 — Schema
    st.markdown('<div class="eyebrow purple">2 — Schema Verification</div>', unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        st.markdown('<div style="font-size:12px;font-weight:600;color:#9d79f5;margin-bottom:8px">Schema Audit — SRI Labs DryQ</div>', unsafe_allow_html=True)
        for s, l, d in [
            ("fail","No Product schema on DryQ PDP","Missing: name, price, availability, AggregateRating"),
            ("fail","No Review / AggregateRating schema","1,079 reviews exist but AI can't access them"),
            ("fail","No FAQ schema despite FAQ section","JSON-LD missing — AI can't lift answers verbatim"),
            ("fail","No VideoObject schema for FOX 5","Earned media invisible to AI without markup"),
            ("fail","No Organization schema","AI doesn't know what brand this is or what it sells"),
        ]:
            st.markdown(f"""<div class="arow"><span class="adot {s}"></span><div><div class="albl">{l}</div><div class="adet">{d}</div></div></div>""", unsafe_allow_html=True)
    with s2:
        schema_df = pd.DataFrame({
            "Schema Type": ["Product + AggregateRating","Organization","FAQ","VideoObject","BreadcrumbList","HowTo"],
            "Priority": ["CRITICAL","CRITICAL","HIGH","HIGH","MED","MED"],
            "AI Impact": ["Shoppable cards","Brand entity","Verbatim citation","FOX 5 credibility","Site structure","Decision support"],
        })
        st.dataframe(schema_df, hide_index=True, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Area 3 — Extractability
    st.markdown('<div class="eyebrow purple">3 — Product Page Extractability</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0f1117;border:1px solid #1c2030;border-radius:10px;padding:18px 20px;margin-bottom:14px">
      <div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:14px">DryQ PDP — Required Content Blocks</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
        <div style="background:#08090d;border:1px solid #1c2030;border-radius:7px;padding:13px 15px">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px">
            <span>📋</span><span style="font-size:13px;font-weight:600;color:#fff">Key Points Summary</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#ef5050;background:rgba(239,80,80,.08);border:1px solid rgba(239,80,80,.2);padding:2px 6px;border-radius:3px">MISSING</span>
          </div>
          <div style="font-size:12px;color:#6b7385;line-height:1.6">3–4 bullets at the top of the PDP. Often the first and only thing AI quotes from a product page.</div>
        </div>
        <div style="background:#08090d;border:1px solid #1c2030;border-radius:7px;padding:13px 15px">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px">
            <span>⚖️</span><span style="font-size:13px;font-weight:600;color:#fff">Pros / Cons</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#ef5050;background:rgba(239,80,80,.08);border:1px solid rgba(239,80,80,.2);padding:2px 6px;border-radius:3px">MISSING</span>
          </div>
          <div style="font-size:12px;color:#6b7385;line-height:1.6">Top AI citation format for purchase-intent queries. "What are the pros and cons of DryQ?" is a common AI search pattern.</div>
        </div>
        <div style="background:#08090d;border:1px solid #1c2030;border-radius:7px;padding:13px 15px">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px">
            <span>📊</span><span style="font-size:13px;font-weight:600;color:#fff">Specs Table</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#f0a500;background:rgba(240,165,0,.08);border:1px solid rgba(240,165,0,.2);padding:2px 6px;border-radius:3px">PARTIAL</span>
          </div>
          <div style="font-size:12px;color:#6b7385;line-height:1.6">AI quotes specific table cells. Move all specs from paragraphs into an HTML table for extraction.</div>
        </div>
        <div style="background:#08090d;border:1px solid #1c2030;border-radius:7px;padding:13px 15px">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px">
            <span>❓</span><span style="font-size:13px;font-weight:600;color:#fff">FAQ Block</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#f0a500;background:rgba(240,165,0,.08);border:1px solid rgba(240,165,0,.2);padding:2px 6px;border-radius:3px">NO SCHEMA</span>
          </div>
          <div style="font-size:12px;color:#6b7385;line-height:1.6">FAQ exists but has no JSON-LD schema. AI can't lift answers as cited responses without the markup.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Area 4 — Robots
    st.markdown('<div class="eyebrow purple">4 — Robots.txt AI Crawler Check</div>', unsafe_allow_html=True)
    rb1, rb2 = st.columns(2)
    with rb1:
        for s, l, d in [
            ("warn","GPTBot — status unverified","Confirm User-agent: GPTBot / Allow: /"),
            ("warn","Bingbot — status unverified","ChatGPT search relies on Bing's index"),
            ("pass","Googlebot — likely allowed","Site ranks in Google — permitted"),
            ("fail","Sitemap not in Bing Webmaster Tools","10-minute fix with direct ChatGPT citation impact"),
        ]:
            st.markdown(f"""<div class="arow"><span class="adot {s}"></span><div><div class="albl">{l}</div><div class="adet">{d}</div></div></div>""", unsafe_allow_html=True)
    with rb2:
        st.code("""# Visit: srilabs.com/robots.txt

# Must NOT be blocked:
User-agent: GPTBot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Googlebot
Allow: /

# Optional: block training, allow indexing
User-agent: CCBot
Disallow: /""", language="text")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Area 5 — FAQ Citation Engine
    st.markdown('<div class="eyebrow purple">5 — FAQ Citation Engine</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:13px;color:#6b7385;line-height:1.65;margin-bottom:16px">
      AI platforms lift FAQ answers verbatim when the format matches a user query. Rule: <strong style="color:#dde1ec">direct question → immediate yes/no → one supporting sentence.</strong> No filler, no hedging.
    </div>
    """, unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    faqs = [
        ("Does infrared hair drying reduce frizz?",
         "Yes. Infrared hair dryers like the SRI DryQ use gentle heat that helps dry hair more evenly, which can reduce frizz compared with traditional dryers. The DryQ's negative ion technology also seals the hair cuticle, eliminating the moisture imbalance that causes frizz."),
        ("How long before I notice results with DryQ?",
         "Most users notice reduced frizz immediately. Improvements in hair thickness from the red light therapy are typically visible within 4–6 weeks of daily use."),
        ("Is red light therapy in hair dryers safe?",
         "Yes. The DryQ emits red light at 650nm — the wavelength clinically studied for hair follicle stimulation. This range is non-ionizing and safe for daily use on all hair types."),
        ("Does SRI DryQ work on thinning hair?",
         "Yes. The 650nm infrared light stimulates blood circulation to the scalp, supporting thicker regrowth over time. 85% of study participants in an independent lab study reported less hair damage."),
    ]
    for i, (q, a) in enumerate(faqs):
        with f1 if i % 2 == 0 else f2:
            st.markdown(f"""<div class="faq-e"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="hyp">💡 Each FAQ above is structured to be quoted verbatim by ChatGPT, Perplexity, or Google AI Overviews. Add FAQ schema (JSON-LD) to convert this section from a buyer-support tool into an active AI citation engine. When a user asks "does infrared drying reduce frizz?" — SRI Labs becomes the cited source.</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close .inner
