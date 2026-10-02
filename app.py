import streamlit as st
import random
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Quantum OS Kernel | CPU Scheduling Simulator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ฟังก์ชันตัวช่วยสำหรับ Render HTML โดยลบช่องว่างนำหน้า (Leading Spaces) ทั้งหมด
# เพื่อป้องกันไม่ให้ Streamlit Markdown เข้าใจผิดว่าเป็น Code Block (<pre><code>)
def render_clean_html(html_str):
    compact_html = "".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(compact_html, unsafe_allow_html=True)


# ==============================================================================
# --- STYLESHEET: CYBERPUNK / HIGH-TECH KERNEL HUD THEME & BOUNCY ANIMATIONS ---
# ==============================================================================
render_clean_html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&family=Prompt:wght@300;400;500;600;700&display=swap');
    
    /* ---------------- Global Reset & Typography ---------------- */
    html, body, [class*="css"], .stApp {
        font-family: 'Prompt', 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    code, pre, .mono-font {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* ---------------- 1. DYNAMIC ANIMATED TECH BACKGROUND ---------------- */
    .stApp {
        background-color: #060911 !important;
        background-image: 
            radial-gradient(circle at 18% 15%, rgba(14, 165, 233, 0.16) 0%, transparent 42%),
            radial-gradient(circle at 82% 28%, rgba(168, 85, 247, 0.16) 0%, transparent 48%),
            radial-gradient(circle at 50% 85%, rgba(16, 185, 129, 0.12) 0%, transparent 50%),
            radial-gradient(rgba(56, 189, 248, 0.15) 1.2px, transparent 1.2px) !important;
        background-size: 100% 100%, 100% 100%, 100% 100%, 36px 36px !important;
        background-attachment: fixed !important;
        color: #e2e8f0 !important;
    }
    
    /* Ambient Light Orbs Animation */
    @keyframes floatOrbA {
        0%, 100% { transform: translate(0px, 0px) scale(1); opacity: 0.6; }
        50% { transform: translate(50px, -35px) scale(1.15); opacity: 0.85; }
    }
    @keyframes floatOrbB {
        0%, 100% { transform: translate(0px, 0px) scale(1); opacity: 0.5; }
        50% { transform: translate(-45px, 40px) scale(1.18); opacity: 0.8; }
    }

    .ambient-orb-1 {
        position: fixed;
        top: -60px;
        left: 5%;
        width: 500px;
        height: 500px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.25) 0%, rgba(59, 130, 246, 0.08) 50%, transparent 70%);
        filter: blur(90px);
        pointer-events: none;
        z-index: 0;
        animation: floatOrbA 16s ease-in-out infinite alternate;
    }

    .ambient-orb-2 {
        position: fixed;
        bottom: 5%;
        right: 5%;
        width: 550px;
        height: 550px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.22) 0%, rgba(236, 72, 153, 0.08) 50%, transparent 70%);
        filter: blur(100px);
        pointer-events: none;
        z-index: 0;
        animation: floatOrbB 18s ease-in-out infinite alternate;
    }

    /* ---------------- 2. BOUNCY & TACTILE BUTTON INTERACTIONS ---------------- */
    @keyframes neonPulse {
        0%, 100% {
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.4), 0 0 30px rgba(99, 102, 241, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }
        50% {
            box-shadow: 0 0 25px rgba(0, 242, 254, 0.7), 0 0 50px rgba(99, 102, 241, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.6);
        }
    }

    /* Base Styling for Streamlit Buttons */
    .stButton > button {
        position: relative;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-family: 'Prompt', 'Outfit', sans-serif !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        color: #F8FAFC !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        overflow: hidden !important;
        letter-spacing: 0.4px !important;
        padding: 10px 22px !important;
    }

    /* Hover Physics: Rise + Scale + Glow */
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        border-color: #38BDF8 !important;
        box-shadow: 0 12px 28px -5px rgba(14, 165, 233, 0.55), 0 0 20px rgba(56, 189, 248, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        color: #FFFFFF !important;
    }

    /* Active Physics: Spring Press Bounce */
    .stButton > button:active {
        transform: translateY(2px) scale(0.95) !important;
        box-shadow: 0 2px 10px rgba(14, 165, 233, 0.4), inset 0 2px 4px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.08s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    /* Light Sweep Shimmer on Button Hover */
    .stButton > button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -60%;
        width: 220%;
        height: 200%;
        background: linear-gradient(60deg, transparent 30%, rgba(255, 255, 255, 0.25) 50%, transparent 70%);
        transform: translateX(-100%);
        transition: transform 0.65s cubic-bezier(0.4, 0, 0.2, 1);
        pointer-events: none;
    }
    .stButton > button:hover::before {
        transform: translateX(100%);
    }

    /* Primary Execution Button (Big Glow & Continuous Energy) */
    .stButton > button[kind="primary"], [data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #0284C7 0%, #6366F1 50%, #A855F7 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.35) !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        letter-spacing: 0.6px !important;
        animation: neonPulse 3s ease-in-out infinite alternate;
    }
    .stButton > button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 50%, #8B5CF6 100%) !important;
        transform: translateY(-4px) scale(1.035) !important;
        box-shadow: 0 16px 36px -6px rgba(0, 242, 254, 0.6), 0 0 30px rgba(139, 92, 246, 0.5) !important;
    }

    /* Secondary / Action Buttons */
    .btn-cyber-print {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 9px 20px;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        color: #38BDF8;
        border: 1.5px solid rgba(56, 189, 248, 0.4);
        border-radius: 12px;
        cursor: pointer;
        font-weight: 700;
        font-size: 13.5px;
        font-family: 'Prompt', sans-serif;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
        text-decoration: none;
    }
    .btn-cyber-print:hover {
        transform: translateY(-3px) scale(1.04);
        background: linear-gradient(135deg, #0284C7 0%, #2563EB 100%);
        color: #FFFFFF;
        border-color: #38BDF8;
        box-shadow: 0 10px 25px -4px rgba(14, 165, 233, 0.6), 0 0 20px rgba(56, 189, 248, 0.4);
    }
    .btn-cyber-print:active {
        transform: translateY(2px) scale(0.95);
        transition: all 0.08s ease;
    }

    /* ---------------- 3. HUD CARDS & CONTAINERS ---------------- */
    .cyber-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(14, 165, 233, 0.12);
        color: #38BDF8;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        border: 1px solid rgba(56, 189, 248, 0.35);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    
    .status-dot-live {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 10px #10B981;
        animation: pulseGreen 1.8s ease-in-out infinite;
    }
    @keyframes pulseGreen {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }

    .cyber-title {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 20%, #E2E8F0 50%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .cyber-subtitle {
        color: #94A3B8;
        font-size: 14px;
        margin-top: 4px;
    }

    /* ---------------- 4. METRIC HUD CARDS ---------------- */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin: 18px 0;
    }

    .metric-hud-box {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 14px;
        padding: 16px 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-hud-box:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.45);
    }
    .metric-hud-box::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3.5px;
        background: linear-gradient(180deg, #00F2FE, #6366F1);
    }
    .metric-hud-box.wt-box::before {
        background: linear-gradient(180deg, #10B981, #059669);
    }
    .metric-hud-box.util-box::before {
        background: linear-gradient(180deg, #F59E0B, #D97706);
    }
    .metric-hud-box.switch-box::before {
        background: linear-gradient(180deg, #EC4899, #8B5CF6);
    }

    .metric-hud-label {
        font-size: 12.5px;
        font-weight: 600;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .metric-hud-value {
        font-size: 26px;
        font-weight: 800;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-hud-unit {
        font-size: 13px;
        font-weight: 500;
        color: #64748B;
        font-family: 'Prompt', sans-serif;
        margin-left: 4px;
    }

    /* ---------------- Streamlit UI Element Overrides ---------------- */
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    .stMarkdown h3, .stMarkdown h4 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px !important;
    }
    
    /* Input Fields & Selectbox */
    [data-testid="stNumberInput"] label, [data-testid="stSelectbox"] label {
        color: #CBD5E1 !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
    }
    [data-testid="stNumberInput"] input {
        background-color: rgba(15, 23, 42, 0.85) !important;
        color: #00F2FE !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stNumberInput"] input:focus {
        border-color: #00F2FE !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.45) !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
    }

    /* Smooth Dark HUD Data Editor Styling */
    div[data-testid="stDataEditor"] {
        background: rgba(13, 20, 36, 0.75) !important;
        border: 1.5px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 14px !important;
        padding: 4px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5) !important;
        overflow: hidden !important;
    }
    div[data-testid="stDataEditor"] canvas {
        border-radius: 10px !important;
    }

    /* ---------------- PRINT LAYOUT STYLING ---------------- */
    @media print {
        header, footer, .stButton, [data-testid="stToolbar"], .ambient-orb-1, .ambient-orb-2 {
            display: none !important;
        }
        .stApp {
            background: #FFFFFF !important;
            color: #000000 !important;
        }
        * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
    }
    </style>
    
    <!-- Dynamic Ambient Lighting Elements -->
    <div class="ambient-orb-1"></div>
    <div class="ambient-orb-2"></div>
""")


# ==============================================================================
# --- HEADER & ACTION BAR ---
# ==============================================================================
col_head, col_action = st.columns([3.8, 1.2])
with col_head:
    render_clean_html("""
        <div>
            <div class="cyber-badge">
                <span class="status-dot-live"></span>
                <span>QUANTUM OS KERNEL • MULTITASKING SCHEDULER</span>
            </div>
            <h1 class="cyber-title">ระบบจำลองการจัดตารางเวลาซีพียูขั้นสูง</h1>
            <p class="cyber-subtitle">High-Precision CPU Scheduling Engine • Real-time Hardware Timeline & Execution Telemetry</p>
        </div>
    """)

with col_action:
    render_clean_html("""
        <div style="text-align: right; padding-top: 20px;">
            <button class="btn-cyber-print" onclick="window.print()">
                <span>🖨️ พิมพ์รายงาน / Export PDF</span>
            </button>
        </div>
    """)


# ==============================================================================
# --- DATA STRUCTURES & COLOR SYSTEM ---
# ==============================================================================
SUBJECTS = [
    "แบบฝึกหัด OS", "รายงาน Database", "โครงงาน Network",
    "สรุป English", "แบบฝึกหัด Math", "เตรียมสอบ IT Security",
    "แล็บ Cloud Computing", "การบ้าน Data Structures",
    "เขียนโปรแกรม Web App", "ออกแบบ UX/UI", "วิจัย Machine Learning", "โครงงาน IoT"
]

# ชุดสี Neon / Cyberpunk High-Tech ประจำ Process P1 - P10 และ Idle
CYBER_PALETTE = {
    "P1":  {
        "gradient": "linear-gradient(135deg, #00F2FE 0%, #0284C7 100%)",
        "border": "#38BDF8",
        "glow": "rgba(0, 242, 254, 0.5)",
        "text": "#041527",
        "accent": "#00F2FE",
        "tag": "CYAN"
    },
    "P2":  {
        "gradient": "linear-gradient(135deg, #F43F5E 0%, #BE123C 100%)",
        "border": "#FB7185",
        "glow": "rgba(244, 63, 94, 0.5)",
        "text": "#FFFFFF",
        "accent": "#F43F5E",
        "tag": "CRIMSON"
    },
    "P3":  {
        "gradient": "linear-gradient(135deg, #10B981 0%, #047857 100%)",
        "border": "#34D399",
        "glow": "rgba(16, 185, 129, 0.5)",
        "text": "#022C19",
        "accent": "#10B981",
        "tag": "EMERALD"
    },
    "P4":  {
        "gradient": "linear-gradient(135deg, #F59E0B 0%, #B45309 100%)",
        "border": "#FBBF24",
        "glow": "rgba(245, 158, 11, 0.5)",
        "text": "#2A1800",
        "accent": "#F59E0B",
        "tag": "AMBER"
    },
    "P5":  {
        "gradient": "linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)",
        "border": "#A78BFA",
        "glow": "rgba(139, 92, 246, 0.5)",
        "text": "#FFFFFF",
        "accent": "#8B5CF6",
        "tag": "VIOLET"
    },
    "P6":  {
        "gradient": "linear-gradient(135deg, #EC4899 0%, #9D174D 100%)",
        "border": "#F472B6",
        "glow": "rgba(236, 72, 153, 0.5)",
        "text": "#FFFFFF",
        "accent": "#EC4899",
        "tag": "MAGENTA"
    },
    "P7":  {
        "gradient": "linear-gradient(135deg, #06B6D4 0%, #0E7490 100%)",
        "border": "#22D3EE",
        "glow": "rgba(6, 182, 212, 0.5)",
        "text": "#02252D",
        "accent": "#06B6D4",
        "tag": "TEAL"
    },
    "P8":  {
        "gradient": "linear-gradient(135deg, #84CC16 0%, #4D7C0F 100%)",
        "border": "#A3E635",
        "glow": "rgba(132, 204, 22, 0.5)",
        "text": "#1A2E05",
        "accent": "#84CC16",
        "tag": "LIME"
    },
    "P9":  {
        "gradient": "linear-gradient(135deg, #FB923C 0%, #C2410C 100%)",
        "border": "#FDBA74",
        "glow": "rgba(251, 146, 60, 0.5)",
        "text": "#2C0F02",
        "accent": "#FB923C",
        "tag": "ORANGE"
    },
    "P10": {
        "gradient": "linear-gradient(135deg, #6366F1 0%, #3730A3 100%)",
        "border": "#818CF8",
        "glow": "rgba(99, 102, 241, 0.5)",
        "text": "#FFFFFF",
        "accent": "#6366F1",
        "tag": "INDIGO"
    },
}

IDLE_STYLE = {
    "gradient": "repeating-linear-gradient(135deg, #0B1120 0px, #0B1120 10px, #1E293B 10px, #1E293B 20px)",
    "border": "#475569",
    "glow": "rgba(71, 85, 105, 0.2)",
    "text": "#94A3B8",
    "accent": "#64748B",
    "tag": "IDLE (HALT)"
}

def get_process_style(p_name):
    if p_name == "Idle":
        return IDLE_STYLE
    if p_name in CYBER_PALETTE:
        return CYBER_PALETTE[p_name]
    palette_list = list(CYBER_PALETTE.values())
    try:
        num = int(''.join(filter(str.isdigit, str(p_name))))
        return palette_list[(num - 1) % len(palette_list)]
    except Exception:
        return palette_list[abs(hash(str(p_name))) % len(palette_list)]


# ==============================================================================
# --- DATA GENERATOR (AT 0-10, BT 1-8, AT=0 AT LEAST 1, OVERLAPPING) ---
# ==============================================================================
def generate_data(seed, count):
    random.seed(seed)
    zero_idx = random.randint(0, count - 1)
    rows = []
    
    subj_pool = SUBJECTS.copy()
    random.shuffle(subj_pool)
    
    for i in range(count):
        at = 0 if i == zero_idx else random.randint(0, 10)
        bt = random.randint(1, 8)
        subj = subj_pool[i % len(subj_pool)]
        rows.append({
            "Process": f"P{i+1}",
            "ชื่องาน / วิชา": subj,
            "AT": at,
            "BT": bt
        })
    
    if all(r["AT"] == rows[0]["AT"] for r in rows) and count > 1:
        other_idx = (zero_idx + 1) % count
        rows[other_idx]["AT"] = random.randint(1, 10)

    return rows


# ==============================================================================
# --- SESSION STATE INITIALIZATION ---
# ==============================================================================
if "seed_val" not in st.session_state:
    st.session_state.seed_val = 1234

if "random_key" not in st.session_state:
    st.session_state.random_key = 0

if "prev_seed" not in st.session_state:
    st.session_state.prev_seed = st.session_state.seed_val

if "num_processes" not in st.session_state:
    st.session_state.num_processes = 5

if "prev_num_processes" not in st.session_state:
    st.session_state.prev_num_processes = st.session_state.num_processes

if "process_list" not in st.session_state:
    st.session_state.process_list = generate_data(st.session_state.seed_val, st.session_state.num_processes)

def on_random_click():
    current_seed = st.session_state.get("seed_val", 1234)
    new_seed = random.randint(1000, 9999)
    while new_seed == current_seed:
        new_seed = random.randint(1000, 9999)
    st.session_state.seed_val = new_seed
    st.session_state.prev_seed = new_seed
    st.session_state.random_key += 1
    st.session_state.process_list = generate_data(new_seed, st.session_state.num_processes)


# ==============================================================================
# --- 1. CONFIGURATION & CONTROL PANEL ---
# ==============================================================================
render_clean_html("<div style='height: 12px;'></div>")
st.markdown("### ⚙️ 1. กำหนดค่าเริ่มต้นและพารามิเตอร์ของระบบ")

col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.2, 1.4])

with col1:
    seed_val = st.number_input("🌱 ค่า Seed (สุ่ม):", step=1, key="seed_val")
with col2:
    quantum_val = st.number_input("⏱️ Time Quantum (q = 1-4):", min_value=1, max_value=4, value=2, step=1)
with col3:
    num_processes = st.selectbox(
        "📋 จำนวนงาน (3 - 10 งาน):",
        options=list(range(3, 11)),
        index=list(range(3, 11)).index(st.session_state.num_processes) if st.session_state.num_processes in range(3, 11) else 2,
        key="num_processes"
    )
with col4:
    st.write("")
    st.write("")
    st.button("🎲 สุ่มโจทย์ใหม่ (RANDOM)", on_click=on_random_click, use_container_width=True)

if st.session_state.prev_seed != seed_val:
    st.session_state.prev_seed = seed_val
    st.session_state.random_key += 1
    st.session_state.process_list = generate_data(seed_val, num_processes)
elif st.session_state.prev_num_processes != num_processes or len(st.session_state.process_list) != num_processes:
    st.session_state.prev_num_processes = num_processes
    st.session_state.random_key += 1
    st.session_state.process_list = generate_data(seed_val, num_processes)


# ==============================================================================
# --- 2. EDITABLE PROCESS QUEUE TABLE ---
# ==============================================================================
render_clean_html("<div style='height: 10px;'></div>")
st.markdown("### 📝 2. รายการงานในคิว (Process Ready Queue - ดับเบิลคลิกเพื่อแก้ไขค่าได้)")
df = pd.DataFrame(st.session_state.process_list)

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed",
    disabled=["Process"],
    key=f"editor_{st.session_state.random_key}"
)
st.session_state.process_list = edited_df.to_dict("records")
processes_input = st.session_state.process_list


# ==============================================================================
# --- 3. SCHEDULING ALGORITHMS (FCFS, SJF-NP, ROUND ROBIN) ---
# ==============================================================================

# 3.1 FCFS
def run_fcfs(procs):
    p_sorted = sorted(procs, key=lambda x: (x["AT"], int(''.join(filter(str.isdigit, str(x["Process"]))))))
    current_time = 0
    gantt = []
    res = {}

    for p in p_sorted:
        p_id = p["Process"]
        at = p["AT"]
        bt = p["BT"]
        
        if current_time < at:
            gantt.append({"Process": "Idle", "start": current_time, "end": at})
            current_time = at
            
        start_t = current_time
        current_time += bt
        ct = current_time
        tat = ct - at
        wt = tat - bt
        
        gantt.append({"Process": p_id, "start": start_t, "end": ct})
        res[p_id] = {"CT": ct, "TAT": tat, "WT": wt}
        
    return gantt, res

# 3.2 SJF (Non-preemptive)
def run_sjf(procs):
    rem_procs = [{**p, "p_num": int(''.join(filter(str.isdigit, str(p["Process"]))))} for p in procs]
    current_time = 0
    completed = 0
    n = len(rem_procs)
    gantt = []
    res = {}
    is_completed = [False] * n

    while completed < n:
        available = [
            (i, p) for i, p in enumerate(rem_procs) 
            if p["AT"] <= current_time and not is_completed[i]
        ]
        
        if not available:
            next_at = min(p["AT"] for i, p in enumerate(rem_procs) if not is_completed[i])
            gantt.append({"Process": "Idle", "start": current_time, "end": next_at})
            current_time = next_at
            continue
            
        available.sort(key=lambda x: (x[1]["BT"], x[1]["AT"], x[1]["p_num"]))
        idx, chosen = available[0]
        
        start_t = current_time
        current_time += chosen["BT"]
        ct = current_time
        tat = ct - chosen["AT"]
        wt = tat - chosen["BT"]
        
        gantt.append({"Process": chosen["Process"], "start": start_t, "end": ct})
        res[chosen["Process"]] = {"CT": ct, "TAT": tat, "WT": wt}
        is_completed[idx] = True
        completed += 1

    return gantt, res

# 3.3 Round Robin (RR)
def run_rr(procs, quantum):
    p_data = [{**p, "rem_bt": p["BT"], "p_num": int(''.join(filter(str.isdigit, str(p["Process"]))))} for p in procs]
    p_data.sort(key=lambda x: (x["AT"], x["p_num"]))
    
    current_time = 0
    queue = []
    gantt = []
    res = {}
    completed = 0
    n = len(p_data)
    arrived = [False] * n

    def check_arrivals(curr_t):
        for i in range(n):
            if not arrived[i] and p_data[i]["AT"] <= curr_t:
                queue.append(p_data[i])
                arrived[i] = True

    check_arrivals(current_time)

    while completed < n:
        if not queue:
            next_at = min(p["AT"] for i, p in enumerate(p_data) if not arrived[i])
            gantt.append({"Process": "Idle", "start": current_time, "end": next_at})
            current_time = next_at
            check_arrivals(current_time)
            continue
            
        curr_p = queue.pop(0)
        run_time = min(quantum, curr_p["rem_bt"])
        start_t = current_time
        current_time += run_time
        curr_p["rem_bt"] -= run_time
        
        gantt.append({"Process": curr_p["Process"], "start": start_t, "end": current_time})
        check_arrivals(current_time)
        
        if curr_p["rem_bt"] == 0:
            ct = current_time
            tat = ct - curr_p["AT"]
            wt = tat - curr_p["BT"]
            res[curr_p["Process"]] = {"CT": ct, "TAT": tat, "WT": wt}
            completed += 1
        else:
            queue.append(curr_p)

    return gantt, res


# ==============================================================================
# --- 4. REALISTIC OS HARDWARE EXECUTION TRACE GANTT CHART ---
# ==============================================================================
def render_gantt_chart(gantt, procs):
    if not gantt:
        return ""
        
    total_time = gantt[-1]["end"]
    busy_time = sum(b["end"] - b["start"] for b in gantt if b["Process"] != "Idle")
    idle_time = total_time - busy_time
    utilization = (busy_time / total_time * 100) if total_time > 0 else 100.0
    switches = max(0, len([b for b in gantt if b["Process"] != "Idle"]) - 1)

    unit_scale = max(60, min(95, int(980 / max(total_time, 1))))
    
    blocks_html = []
    n = len(gantt)
    
    for i, block in enumerate(gantt):
        p_name = block["Process"]
        st_t = block["start"]
        en_t = block["end"]
        duration = en_t - st_t
        width = duration * unit_scale
        
        style = get_process_style(p_name)
        gradient = style["gradient"]
        text_color = style["text"]
        border_color = style["border"]
        glow_color = style["glow"]
        
        is_first = (i == 0)
        is_last = (i == n - 1)
        
        p_obj = next((p for p in procs if p["Process"] == p_name), None)
        task_label = p_obj['ชื่องาน / วิชา'] if p_obj else ""
        
        if p_name == "Idle":
            inner_content = f"""
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;width:100%;padding:4px;box-sizing:border-box;">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;color:#94A3B8;letter-spacing:0.5px;">💤 SYSTEM IDLE</div>
                    <div style="font-size:10.5px;color:#64748B;font-weight:600;font-family:'JetBrains Mono',monospace;">Δ {duration}t (HALT)</div>
                </div>
            """
            custom_border = "border: 1.5px dashed #475569;"
            custom_bg = f"background: {gradient};"
            custom_glow = "box-shadow: inset 0 0 12px rgba(0,0,0,0.5);"
        else:
            show_full = width >= 85
            task_snippet = f"<div style='font-size:11.5px;font-weight:600;opacity:0.95;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:92%;'>{task_label}</div>" if show_full else ""
            
            inner_content = f"""
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;width:100%;padding:4px 6px;box-sizing:border-box;position:relative;">
                    <div style="display:flex;align-items:center;justify-content:space-between;width:92%;margin-bottom:2px;">
                        <span style="font-family:'JetBrains Mono',monospace;font-size:13.5px;font-weight:800;">{p_name}</span>
                        <span style="font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;opacity:0.85;background:rgba(0,0,0,0.2);padding:1px 5px;border-radius:5px;">Δ{duration}t</span>
                    </div>
                    {task_snippet}
                    <div style="font-size:10px;font-family:'JetBrains Mono',monospace;opacity:0.75;margin-top:1px;">[{st_t} → {en_t}]</div>
                </div>
            """
            custom_border = f"border: 1px solid {border_color};"
            custom_bg = f"background: {gradient};"
            custom_glow = f"box-shadow: 0 4px 16px {glow_color}, inset 0 1px 1px rgba(255,255,255,0.45);"

        tooltip = f"Process: {p_name} | งาน: {task_label} | ช่วงเวลา: {st_t} → {en_t} (รวม {duration} หน่วยเวลา)"

        bar_box = f"""
            <div title="{tooltip}" style="height:56px;width:100%;{custom_bg}color:{text_color};{custom_border}{custom_glow}border-radius:8px;cursor:pointer;user-select:none;position:relative;overflow:hidden;">
                <div style="position:absolute;top:0;left:0;right:0;height:42%;background:linear-gradient(180deg,rgba(255,255,255,0.3) 0%,rgba(255,255,255,0.02) 100%);pointer-events:none;"></div>
                {inner_content}
            </div>
        """
        
        first_tick = ""
        if is_first:
            first_tick = f"""
                <div style="position:absolute;left:0px;top:58px;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;pointer-events:none;z-index:5;">
                    <div style="width:2px;height:10px;background:#38BDF8;box-shadow:0 0 6px #38BDF8;"></div>
                    <span style="font-size:11.5px;font-weight:700;color:#38BDF8;margin-top:3px;font-family:'JetBrains Mono',monospace;background:#0B132B;padding:1px 5px;border-radius:5px;border:1px solid rgba(56,189,248,0.4);">{st_t}</span>
                </div>
            """
            
        end_tick = f"""
            <div style="position:absolute;right:0px;top:58px;transform:translateX(50%);display:flex;flex-direction:column;align-items:center;pointer-events:none;z-index:5;">
                <div style="width:2px;height:10px;background:#38BDF8;box-shadow:0 0 6px #38BDF8;"></div>
                <span style="font-size:11.5px;font-weight:700;color:#38BDF8;margin-top:3px;font-family:'JetBrains Mono',monospace;background:#0B132B;padding:1px 5px;border-radius:5px;border:1px solid rgba(56,189,248,0.4);">{en_t}</span>
            </div>
        """
        
        block_html = f"""
            <div style="flex-shrink:0;width:{width}px;position:relative;box-sizing:border-box;margin-right:2px;">
                {bar_box}{first_tick}{end_tick}
            </div>
        """
        blocks_html.append(block_html)
        
    gantt_inner = "".join(blocks_html)
    
    # Legend สไตล์ Cyber Tags
    legend_items = []
    used_procs = sorted(list({b["Process"] for b in gantt if b["Process"] != "Idle"}), key=lambda x: int(''.join(filter(str.isdigit, str(x)))))
    for p_id in used_procs:
        st_info = get_process_style(p_id)
        p_obj = next((p for p in procs if p["Process"] == p_id), None)
        sub_name = f" • {p_obj['ชื่องาน / วิชา']}" if p_obj else ""
        item_html = f"""
            <span style="display:inline-flex;align-items:center;gap:6px;background:rgba(15,23,42,0.9);color:#E2E8F0;padding:4px 12px;border-radius:8px;font-size:12px;font-weight:600;border:1px solid {st_info['border']};margin:3px 4px;box-shadow:0 2px 8px rgba(0,0,0,0.3);">
                <span style="width:8px;height:8px;border-radius:2px;background:{st_info['accent']};box-shadow:0 0 6px {st_info['accent']};"></span>
                <span style="color:{st_info['border']};font-family:'JetBrains Mono',monospace;font-weight:700;">{p_id}</span>{sub_name}
            </span>
        """
        legend_items.append(item_html)
        
    if any(b["Process"] == "Idle" for b in gantt):
        item_html = """
            <span style="display:inline-flex;align-items:center;gap:6px;background:rgba(15,23,42,0.9);color:#94A3B8;padding:4px 12px;border-radius:8px;font-size:12px;font-weight:600;border:1px dashed #64748B;margin:3px 4px;">
                <span style="width:8px;height:8px;border-radius:2px;background:#64748B;"></span>
                <span>IDLE (CPU พักการทำงาน)</span>
            </span>
        """
        legend_items.append(item_html)
        
    legend_html = "".join(legend_items)
    
    chart_container = f"""
        <div style="background:rgba(11,17,32,0.85);border:1.5px solid rgba(56,189,248,0.22);border-radius:16px;padding:18px 22px 28px 22px;box-shadow:0 10px 30px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.06);margin-bottom:22px;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;margin-bottom:16px;gap:10px;border-bottom:1px solid rgba(255,255,255,0.07);padding-bottom:12px;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="display:flex;align-items:center;gap:6px;background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.4);padding:3px 10px;border-radius:6px;">
                        <span class="status-dot-live"></span>
                        <span style="font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;color:#34D399;letter-spacing:0.5px;">CORE #0 • EXECUTION PIPELINE</span>
                    </div>
                    <span style="font-size:12.5px;color:#94A3B8;font-weight:500;">ไทม์ไลน์การทำงานจริงของซีพียู (Hardware Trace)</span>
                </div>
                <div style="display:flex;align-items:center;gap:14px;font-family:'JetBrains Mono',monospace;font-size:12px;">
                    <span style="color:#94A3B8;">⏱️ Total: <strong style="color:#F8FAFC;">{total_time}t</strong></span>
                    <span style="color:#94A3B8;">🔥 CPU Load: <strong style="color:#38BDF8;">{utilization:.1f}%</strong></span>
                    <span style="color:#94A3B8;">🔄 Switches: <strong style="color:#F472B6;">{switches}</strong></span>
                </div>
            </div>
            <div style="display:flex;flex-wrap:wrap;margin-bottom:16px;">
                {legend_html}
            </div>
            <div style="overflow-x:auto;padding:12px 10px 38px 10px;background:rgba(6,11,22,0.6);border-radius:12px;border:1px solid rgba(255,255,255,0.05);">
                <div style="display:inline-flex;flex-direction:row;margin:6px 20px 10px 20px;position:relative;">
                    {gantt_inner}
                </div>
            </div>
        </div>
    """
    return chart_container


# ==============================================================================
# --- 5. RESULT DISPLAY & HUD METRICS ---
# ==============================================================================
def render_results_table(procs, res):
    rows_html = []
    tot_tat = 0
    tot_wt = 0
    
    for p in procs:
        p_id = p["Process"]
        c = res[p_id]["CT"]
        t = res[p_id]["TAT"]
        w = res[p_id]["WT"]
        tot_tat += t
        tot_wt += w
        
        st_info = get_process_style(p_id)
        
        row_html = f"""
            <tr style="border-bottom:1px solid rgba(255,255,255,0.06);background:rgba(15,23,42,0.6);">
                <td style="padding:10px 14px;text-align:center;">
                    <span style="display:inline-block;padding:2px 10px;border-radius:6px;font-weight:800;font-family:'JetBrains Mono',monospace;font-size:13px;background:{st_info['gradient']};color:{st_info['text']};box-shadow:0 2px 8px {st_info['glow']};">
                        {p_id}
                    </span>
                </td>
                <td style="padding:10px 14px;color:#F1F5F9;font-weight:600;font-size:13.5px;">{p['ชื่องาน / วิชา']}</td>
                <td style="padding:10px 14px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:13.5px;color:#94A3B8;">{p['AT']}</td>
                <td style="padding:10px 14px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:13.5px;color:#94A3B8;">{p['BT']}</td>
                <td style="padding:10px 14px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:13.5px;color:#38BDF8;font-weight:700;">{c}</td>
                <td style="padding:10px 14px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:13.5px;color:#A78BFA;font-weight:700;">{t}</td>
                <td style="padding:10px 14px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:13.5px;color:#34D399;font-weight:700;">{w}</td>
            </tr>
        """
        rows_html.append(row_html)
        
    table_html = f"""
        <div style="background:rgba(13,20,36,0.75);border:1.5px solid rgba(56,189,248,0.22);border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);margin:16px 0 22px 0;">
            <table style="width:100%;border-collapse:collapse;text-align:left;">
                <thead>
                    <tr style="background:linear-gradient(135deg,rgba(30,41,59,0.9) 0%,rgba(15,23,42,0.98) 100%);border-bottom:1.5px solid rgba(56,189,248,0.25);">
                        <th style="padding:12px 14px;text-align:center;color:#38BDF8;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;letter-spacing:0.5px;">PROCESS</th>
                        <th style="padding:12px 14px;color:#CBD5E1;font-size:12.5px;font-weight:700;">ชื่องาน / วิชา</th>
                        <th style="padding:12px 14px;text-align:center;color:#94A3B8;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;">AT (มาถึง)</th>
                        <th style="padding:12px 14px;text-align:center;color:#94A3B8;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;">BT (เวลา)</th>
                        <th style="padding:12px 14px;text-align:center;color:#38BDF8;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;">CT (เสร็จที่)</th>
                        <th style="padding:12px 14px;text-align:center;color:#A78BFA;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;">TAT (CT - AT)</th>
                        <th style="padding:12px 14px;text-align:center;color:#34D399;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;">WT (TAT - BT)</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows_html)}
                </tbody>
            </table>
        </div>
    """
    return table_html, tot_tat, tot_wt

def display_results(title, gantt, res, procs):
    render_clean_html(f"#### ⚡ ผลลัพธ์การประมวลผล: <span style='color: #38BDF8;'>{title}</span>")
    
    # 1. Gantt Chart ระดับ Hardware Profiler (แสดงผลเป็น HTML สะอาด ไม่มีปัญหากล่อง Code สีขาว)
    chart_html = render_gantt_chart(gantt, procs)
    render_clean_html(chart_html)
    
    # 2. ตารางผลลัพธ์แบบ Dark Glass HUD Table (เนียนไปกับพื้นหลัง ไม่เป็นสี่เหลี่ยมสีขาวแปะ)
    table_html, tot_tat, tot_wt = render_results_table(procs, res)
    render_clean_html(table_html)
    
    # 3. คำนวณค่าเฉลี่ย
    avg_tat = tot_tat / len(procs)
    avg_wt = tot_wt / len(procs)
    total_time = gantt[-1]["end"] if gantt else 1
    busy_time = sum(b["end"] - b["start"] for b in gantt if b["Process"] != "Idle")
    utilization = (busy_time / total_time * 100) if total_time > 0 else 100.0
    switches = max(0, len([b for b in gantt if b["Process"] != "Idle"]) - 1)
    
    # 4. HUD Metric Cards แบบ Cyberpunk
    metric_cards_html = f"""
        <div class="metric-grid">
            <div class="metric-hud-box">
                <div class="metric-hud-label">⏱️ Turnaround Time เฉลี่ย (Avg TAT)</div>
                <div class="metric-hud-value">{avg_tat:.2f} <span class="metric-hud-unit">หน่วยเวลา</span></div>
            </div>
            <div class="metric-hud-box wt-box">
                <div class="metric-hud-label">⏳ Waiting Time เฉลี่ย (Avg WT)</div>
                <div class="metric-hud-value">{avg_wt:.2f} <span class="metric-hud-unit">หน่วยเวลา</span></div>
            </div>
            <div class="metric-hud-box util-box">
                <div class="metric-hud-label">🔥 CPU Utilization (ประสิทธิภาพ)</div>
                <div class="metric-hud-value">{utilization:.1f}% <span class="metric-hud-unit">Active</span></div>
            </div>
            <div class="metric-hud-box switch-box">
                <div class="metric-hud-label">🔄 Context Switches (การสลับงาน)</div>
                <div class="metric-hud-value">{switches} <span class="metric-hud-unit">ครั้ง</span></div>
            </div>
        </div>
        <hr style="border: none; border-top: 1px solid rgba(56, 189, 248, 0.15); margin: 28px 0;">
    """
    render_clean_html(metric_cards_html)


# ==============================================================================
# --- 6. SIMULATION EXECUTION TRIGGER ---
# ==============================================================================
render_clean_html("<div style='height: 10px;'></div>")
st.markdown("### 🚀 3. การประมวลผลและวิเคราะห์เปรียบเทียบ")

if st.button("⚡ เริ่มการจำลองและคำนวณเปรียบเทียบทั้ง 3 อัลกอริทึม (EXECUTE ALL)", type="primary", use_container_width=True):
    g_fcfs, r_fcfs = run_fcfs(processes_input)
    display_results("FCFS (First-Come, First-Served)", g_fcfs, r_fcfs, processes_input)
    
    g_sjf, r_sjf = run_sjf(processes_input)
    display_results("SJF (Shortest Job First - Non-preemptive)", g_sjf, r_sjf, processes_input)
    
    g_rr, r_rr = run_rr(processes_input, quantum_val)
    display_results(f"Round Robin (Time Quantum = {quantum_val})", g_rr, r_rr, processes_input)
