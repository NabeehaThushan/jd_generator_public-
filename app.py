import streamlit as st
import openai
import time

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JD Generator — Write JDs That Actually Filter",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #0a0a0f;
    color: #e8e4dc;
}

/* Hero */
.hero {
    padding: 60px 0 40px;
    text-align: center;
}
.hero-tag {
    display: inline-block;
    background: rgba(255,213,0,0.12);
    border: 1px solid rgba(255,213,0,0.3);
    color: #ffd500;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 6px 16px;
    border-radius: 20px;
    margin-bottom: 24px;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 800;
    color: #f0ece4;
    line-height: 1.05;
    margin: 0 0 16px;
}
.hero h1 span {
    color: #ffd500;
}
.hero p {
    font-size: 17px;
    color: #7a7570;
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.7;
}

/* Stats bar */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 48px;
    padding: 32px 0;
    border-top: 1px solid rgba(255,255,255,0.06);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin: 32px 0 48px;
}
.stat { text-align: center; }
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #ffd500;
    display: block;
}
.stat-label {
    font-size: 12px;
    color: #5a5550;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Section labels */
.section-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #ffd500;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,213,0,0.2);
}

/* Cards */
.card {
    background: #111118;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 16px;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #f0ece4;
    margin-bottom: 4px;
}
.card-sub {
    font-size: 13px;
    color: #5a5550;
    margin-bottom: 20px;
}

/* Streamlit inputs override */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #16161e !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(255,213,0,0.4) !important;
    box-shadow: 0 0 0 3px rgba(255,213,0,0.08) !important;
}
label, .stTextInput label, .stTextArea label, .stSelectbox label {
    color: #9a9590 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* Buttons */
.stButton > button {
    background: #ffd500 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 14px 32px !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #ffe840 !important;
    transform: translateY(-1px) !important;
}

/* Output box */
.output-box {
    background: #0e0e14;
    border: 1px solid rgba(255,213,0,0.2);
    border-radius: 16px;
    padding: 32px;
    font-size: 15px;
    line-height: 1.8;
    color: #d8d4cc;
    white-space: pre-wrap;
    position: relative;
}
.output-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.output-badge {
    background: rgba(34,197,94,0.15);
    border: 1px solid rgba(34,197,94,0.3);
    color: #22c55e;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
}

/* Changed tags styling */
.changed-highlight {
    background: rgba(255,213,0,0.15);
    border-left: 3px solid #ffd500;
    padding: 8px 12px;
    margin: 8px 0;
    border-radius: 0 8px 8px 0;
}

/* Role type pills */
.role-pills {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 8px;
}

/* Warning box */
.warn-box {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #f87171;
    margin-bottom: 16px;
}

/* Step indicator */
.step-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #7a7570;
    margin-bottom: 24px;
}
.step-dot {
    width: 8px;
    height: 8px;
    background: #ffd500;
    border-radius: 50%;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 32px 0;
}

/* Metrics row */
.metrics-row {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
}
.metric-chip {
    background: rgba(255,213,0,0.08);
    border: 1px solid rgba(255,213,0,0.2);
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 12px;
    color: #ffd500;
    font-weight: 500;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a35; border-radius: 3px; }

/* Hide streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1100px; }
</style>
""", unsafe_allow_html=True)

# ─── Prompts ───────────────────────────────────────────────────────────────────
ROLE_EXTRA = {
    "Technical (Engineer / DevOps / SRE)": """
Additional rules for technical roles:
- State the system's scale (RPS, data volume, user count) if provided
- Describe the current architecture in 2-3 sentences if known
- Name the main technical problem this role will solve
- Specify the level of autonomy: are tasks given or problems""",

    "Product (PM / Designer / Analyst)": """
Additional rules for product roles:
- Describe the product: who the users are, what problem it solves
- State the key metrics this role affects
- Describe the decision-making process (data-driven, founder-driven)
- Name the most significant recent product decision if known""",

    "Leadership (Team Lead / Head of / VP / CTO)": """
Additional rules for leadership roles:
- Describe the company stage and current team size
- Name 2-3 strategic priorities for the next year if provided
- Define expectations for the role at 6 and 12 months""",

    "Sales / Customer Success / Marketing": """
Additional rules for non-technical roles:
- Replace 'stack' with 'toolset and process' (CRM, outreach tools)
- State measurable outcome expected in the first 90 days
- Forbidden phrases expanded: also ban 'results-oriented', 'self-starter', 'passionate', 'go-getter'""",
}

GENERATION_SYSTEM = """You are a technical recruiter with 10 years of IT hiring experience. You write job descriptions that filter candidates, not attract volume.

RULES:
- Start with 2-3 sentences about the ACTUAL TASK, not the company
- Split requirements into "Required" (max 5) and "Nice to Have" (max 5)
- Describe 3-5 specific tasks for the FIRST 90 DAYS — concrete, not vague
- Include team size, work format, production stack
- If salary is provided, include it. If not, leave a [SALARY RANGE] placeholder
- Include an "Anti-requirements" section: 2-3 sentences on who this role is NOT for
- FORBIDDEN WORDS/PHRASES — never use these: "fast-growing", "market leader", "proactive", "multitasking", "fast-paced environment", "dynamic", "innovative", "passionate", "rockstar", "ninja", "competitive salary", "unique opportunity", "cutting-edge", "world-class", "synergy", "leverage", "best-in-class"
- Tone: direct, concrete, respectful — no hype
- Length: 400-550 words"""

REVIEW_SYSTEM = """You are a senior hiring consultant reviewing a job description for quality and filtering effectiveness.

Analyze the job description below against these criteria and return a REVISED version:

1. SPECIFICITY: Can the candidate understand what they'll be doing in month 1? Fix vague language.
2. FILTERING: Will unqualified candidates self-select out? Tighten if not.
3. CLICHÉS: Find any phrases that carry no real information and replace them.
4. REQUIREMENTS BALANCE: Are ALL required criteria realistically findable in one person? Move excess to nice-to-have.
5. TRANSPARENCY: Are there conditions whose omission will cause offer-stage rejections? Add placeholders.

Mark every change with [CHANGED] tag inline so the reviewer can spot edits.
Return only the revised job description, no preamble."""


def call_openai(system: str, user: str, api_key: str, model: str) -> str:
    client = openai.OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.7,
        max_tokens=1500,
    )
    return resp.choices[0].message.content


def build_context(data: dict) -> str:
    return f"""
Role title: {data['role_title']}
Role type: {data['role_type']}
Reason this role opened: {data['reason']}
First 90-day tasks: {data['tasks']}
Production stack / toolset: {data['stack']}
Team context: {data['team']}
Required skills (hiring manager's list): {data['must_have']}
Nice to have: {data['nice_to_have']}
Work format & conditions: {data['conditions']}
Salary range: {data.get('salary', 'Not specified')}
Anti-requirements (who should NOT apply): {data.get('anti_req', 'Not specified')}
Past hiring failures / false positives to avoid: {data.get('anti_patterns', 'None specified')}
"""


# ─── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">✦ JD Generator</div>
  <h1>Job descriptions that<br><span>filter</span>, not just attract.</h1>
  <p>78% of applications come from unqualified candidates. Vague JDs are the cause. This fixes that.</p>
</div>

<div class="stats-bar">
  <div class="stat"><span class="stat-num">78%</span><span class="stat-label">Apps are unqualified</span></div>
  <div class="stat"><span class="stat-num">23h</span><span class="stat-label">Wasted screening / week</span></div>
  <div class="stat"><span class="stat-num">2×</span><span class="stat-label">Review passes per JD</span></div>
  <div class="stat"><span class="stat-num">40–60%</span><span class="stat-label">Target relevant rate</span></div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar: API settings ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o"],
        index=0,
        help="gpt-4o-mini: ~$0.001/JD  |  gpt-4o: ~$0.02/JD"
    )
    st.caption(f"**Cost estimate:** {'~$0.001 per JD' if model == 'gpt-4o-mini' else '~$0.02 per JD'}")
    st.markdown("---")
    st.markdown("**How it works:**")
    st.markdown("1. Fill the intake form")
    st.markdown("2. Step 1 — generates JD from your context")
    st.markdown("3. Step 2 — critical review pass")
    st.markdown("4. Copy final output")

# ─── Main layout: 2 cols ──────────────────────────────────────────────────────
col_form, col_out = st.columns([1, 1], gap="large")

with col_form:
    st.markdown('<div class="section-label">01 — Intake Form</div>', unsafe_allow_html=True)

    role_title = st.text_input("Role Title *", placeholder="e.g. Backend Engineer (Python), Head of Product")
    role_type = st.selectbox("Role Type *", list(ROLE_EXTRA.keys()))

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">02 — Context</div>', unsafe_allow_html=True)

    reason = st.text_area(
        "Why did this role open? *",
        placeholder="e.g. Growth — current backend team of 3 can't handle new payment system load. Not a backfill.",
        height=80,
    )
    tasks = st.text_area(
        "3–5 specific tasks for the first 90 days *",
        placeholder="e.g.\n1. Migrate billing module from monolith to event-driven (Kafka + Postgres)\n2. Reduce API latency from 1.2s to <300ms on payment endpoints\n3. Set up load testing with Locust for top 5 critical flows",
        height=130,
    )
    stack = st.text_area(
        "Production stack / toolset (what's actually used daily)",
        placeholder="e.g. Python 3.11, FastAPI, PostgreSQL 15, Redis, AWS ECS, GitHub Actions",
        height=80,
    )
    team = st.text_area(
        "Team context",
        placeholder="e.g. 4 backend devs, 1 DevOps, 1 QA. Architecture decisions made by the team. Weekly planning, async otherwise.",
        height=80,
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">03 — Requirements</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        must_have = st.text_area(
            "Must-have (max 5) *",
            placeholder="1. 3+ yrs Python in prod\n2. PostgreSQL at scale\n3. Event-driven patterns\n4. Monolith decomposition exp",
            height=140,
        )
    with c2:
        nice_to_have = st.text_area(
            "Nice to have (max 5)",
            placeholder="1. FastAPI in prod\n2. Kafka/RabbitMQ\n3. AWS ECS/RDS\n4. Load testing exp",
            height=140,
        )

    salary = st.text_input("Salary range", placeholder="e.g. $90–120K, review after 6 months  |  Leave blank to add placeholder")
    conditions = st.text_area(
        "Work format & conditions",
        placeholder="e.g. Remote, 2 syncs/week (9am ET). Overlap required 10am–2pm ET.",
        height=70,
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">04 — Filters</div>', unsafe_allow_html=True)

    anti_req = st.text_area(
        "Anti-requirements — who should NOT apply",
        placeholder="e.g. Not suitable if you're looking for a greenfield project with no legacy code, or a role with minimal cross-team communication.",
        height=80,
    )
    anti_patterns = st.text_area(
        "Past hiring failures / signals to avoid (optional)",
        placeholder="e.g. Last hire knew Kafka but had no experience with legacy systems — caused 3-month onboarding delay.",
        height=70,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if not api_key:
        st.markdown('<div class="warn-box">⚠️ Add your OpenAI API key in the sidebar to generate.</div>', unsafe_allow_html=True)

    generate_btn = st.button("✦ Generate Job Description", disabled=not api_key)

# ─── Output column ─────────────────────────────────────────────────────────────
with col_out:
    st.markdown('<div class="section-label">05 — Output</div>', unsafe_allow_html=True)

    output_placeholder = st.empty()

    if "step1_output" not in st.session_state:
        st.session_state.step1_output = ""
    if "step2_output" not in st.session_state:
        st.session_state.step2_output = ""
    if "generating" not in st.session_state:
        st.session_state.generating = False

    if generate_btn:
        # Validate
        missing = []
        if not role_title: missing.append("Role Title")
        if not reason: missing.append("Why role opened")
        if not tasks: missing.append("First 90-day tasks")
        if not must_have: missing.append("Must-have requirements")

        if missing:
            st.error(f"Please fill in: {', '.join(missing)}")
        else:
            form_data = {
                "role_title": role_title,
                "role_type": role_type,
                "reason": reason,
                "tasks": tasks,
                "stack": stack or "Not specified",
                "team": team or "Not specified",
                "must_have": must_have,
                "nice_to_have": nice_to_have or "None specified",
                "conditions": conditions or "Not specified",
                "salary": salary or "Not specified — use placeholder",
                "anti_req": anti_req or "Not specified",
                "anti_patterns": anti_patterns or "None",
            }

            system_prompt = GENERATION_SYSTEM + ROLE_EXTRA[role_type]
            context = build_context(form_data)

            with output_placeholder.container():
                st.markdown("""
                <div class="step-indicator">
                  <div class="step-dot"></div>
                  Step 1 of 2 — Generating job description from your context...
                </div>""", unsafe_allow_html=True)

            try:
                step1 = call_openai(system_prompt, context, api_key, model)
                st.session_state.step1_output = step1

                with output_placeholder.container():
                    st.markdown("""
                    <div class="step-indicator">
                      <div class="step-dot"></div>
                      Step 2 of 2 — Running critical review pass...
                    </div>""", unsafe_allow_html=True)

                step2 = call_openai(
                    REVIEW_SYSTEM,
                    f"Review and improve this job description:\n\n{step1}",
                    api_key,
                    model,
                )
                st.session_state.step2_output = step2

            except Exception as e:
                st.error(f"API error: {e}")

    # Show outputs
    if st.session_state.step1_output or st.session_state.step2_output:
        with output_placeholder.container():
            tab1, tab2 = st.tabs(["✦ Final (After Review)", "Draft (Before Review)"])

            with tab1:
                if st.session_state.step2_output:
                    st.markdown(f"""
                    <div class="output-box">
                      <div class="output-header">
                        <span style="font-family:'Syne',sans-serif;font-weight:700;color:#f0ece4;">
                          {role_title or "Job Description"}
                        </span>
                        <span class="output-badge">✓ Reviewed</span>
                      </div>
                      {st.session_state.step2_output.replace('[CHANGED]', '<span style="background:rgba(255,213,0,0.2);padding:1px 4px;border-radius:3px;font-size:11px;color:#ffd500;font-weight:600;margin-left:4px">[CHANGED]</span>')}
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.download_button(
                        "⬇ Download as .txt",
                        data=st.session_state.step2_output,
                        file_name=f"jd_{role_title.replace(' ', '_').lower()}.txt",
                        mime="text/plain",
                    )

            with tab2:
                if st.session_state.step1_output:
                    st.markdown(f"""
                    <div class="output-box" style="border-color:rgba(255,255,255,0.1);">
                      <div class="output-header">
                        <span style="font-family:'Syne',sans-serif;font-weight:700;color:#7a7570;">Draft Output</span>
                        <span style="font-size:11px;color:#5a5550;">Before review pass</span>
                      </div>
                      {st.session_state.step1_output}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        with output_placeholder.container():
            st.markdown("""
            <div style="
                border: 2px dashed rgba(255,255,255,0.06);
                border-radius: 16px;
                padding: 64px 32px;
                text-align: center;
                color: #3a3530;
            ">
                <div style="font-size:48px;margin-bottom:16px;">✦</div>
                <div style="font-family:'Syne',sans-serif;font-size:18px;color:#4a4540;margin-bottom:8px;">
                    Your JD will appear here
                </div>
                <div style="font-size:14px;color:#3a3530;">
                    Fill the form → click Generate<br>Two AI passes run automatically
                </div>
            </div>
            """, unsafe_allow_html=True)
