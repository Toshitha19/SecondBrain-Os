import streamlit as st
import requests
import json

# Configuration
API_URL = "http://localhost:8000/audit"

st.set_page_config(
    page_title="SecondBrain OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Premium" feel
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTextInput>div>div>input {
        background-color: #262730;
        color: #FAFAFA;
    }
    .stTextArea>div>div>textarea {
        background-color: #262730;
        color: #FAFAFA;
    }
    .metric-card {
        background-color: #262730;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #4B5563;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 SecondBrain OS")
st.subheader("Decision Integrity & Cognitive Bias Auditing System")

# storage for report (session state)
if 'report' not in st.session_state:
    st.session_state['report'] = None

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("Decision Context")
    
    domain = st.selectbox(
        "Domain",
        ["general", "career", "finance", "health"]
    )
    
    time_horizon = st.select_slider(
        "Time Horizon",
        options=["short", "medium", "long"]
    )
    
    values_input = st.text_area(
        "Core Values (comma separated)",
        placeholder="e.g., freedom, security, family, innovation",
        help="List your top values to check alignment."
    )

# --- MAIN INPUT ---
decision_text = st.text_area(
    "What decision are you facing?",
    placeholder="e.g., I am considering quitting my stable job to start a bakery...",
    height=150
)

# --- AUDIT BUTTON ---
if st.button("Audit Decision", type="primary", use_container_width=True):
    if not decision_text:
        st.error("Please enter a decision to audit.")
    else:
        values_list = [v.strip() for v in values_input.split(",") if v.strip()]
        
        payload = {
            "decision_text": decision_text,
            "domain": domain,
            "time_horizon": time_horizon,
            "values": values_list
        }
        
        with st.spinner("Auditing decision... Analyzing biases... Simulating futures..."):
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    st.session_state['report'] = response.json()
                    st.success("Audit Complete.")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# --- REPORT DISPLAY ---
report = st.session_state['report']

if report:
    st.markdown("---")
    st.header("Decision Audit Report")
    
    # 1. SCORES
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Risk Exposure</h3>
            <h1 style="color: {'#FF4B4B' if report['risk_score'] > 70 else '#FAFAFA'}">{report['risk_score']}/100</h1>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Cognitive Clarity</h3>
            <h1 style="color: {'#FFA500' if report['bias_score'] < 50 else '#FAFAFA'}">{report['bias_score']}/100</h1>
            <p>(Inverse of Bias)</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Value Alignment</h3>
            <h1 style="color: {'#00CC96' if report['alignment_score'] > 80 else '#FAFAFA'}">{report['alignment_score']}/100</h1>
        </div>
        """, unsafe_allow_html=True)

    # 2. BIASES
    st.markdown("### 🔍 Detected Biases")
    biases = report.get('bias_analysis', {}).get('biases', [])
    if not biases:
        st.info("No significant biases detected.")
    else:
        for b in biases:
            with st.expander(f"{b['bias_type']} ({b['severity'].upper()})"):
                st.write(f"**Evidence:** \"{b['evidence']}\"")

    # 3. DECOMPOSITION
    st.markdown("### 🧩 Decision Components")
    decomp = report.get('decomposition', {})
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Objective:**", decomp.get('objective'))
        st.write("**Risk Tolerance:**", decomp.get('risk_tolerance'))
        st.write("**Irreversible Factors:**")
        for f in decomp.get('irreversible_factors', []):
            st.markdown(f"- {f}")
            
    with c2:
        st.write("**Assumptions:**")
        for a in decomp.get('assumptions', []):
            st.markdown(f"- {a}")
        st.write("**Emotional Signals:**")
        for e in decomp.get('emotional_signals', []):
            st.markdown(f"- {e}")

    # 4. SIMULATION
    st.markdown("### 🔮 Future Scenarios")
    sim = report.get('simulation', {}).get('scenarios', {})
    
    tab1, tab2, tab3, tab4 = st.tabs(["Most Likely", "Best Case", "Worst Case", "Long Term"])
    
    with tab1:
        st.info(sim.get('most_likely'))
    with tab2:
        st.success(sim.get('best_case'))
    with tab3:
        st.error(sim.get('worst_case'))
    with tab4:
        st.warning(sim.get('long_term'))

    # 5. INTEGRITY & REFLECTION
    st.markdown("### ⚖️ Value Alignment & Reflection")
    
    # Conflicts
    conflicts = report.get('integrity_analysis', {}).get('conflicts', [])
    if conflicts:
        st.markdown("#### Conflicts Detected:")
        for c in conflicts:
            st.warning(f"**{c['value']}**: {c['conflict_reason']}")
    else:
        st.success("No direct value conflicts detected.")
        
    # Reflection Questions
    st.markdown("#### 🤔 Reflection Questions")
    for q in report.get('reflection_questions', []):
        st.markdown(f"> *{q}*")

    st.markdown("---")
    st.caption("SecondBrain OS - Non-Prescriptive AI Decision Support System")
