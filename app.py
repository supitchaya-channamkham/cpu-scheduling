import streamlit as st
import random
import pandas as pd
import altair as alt
import streamlit.components.v1 as components

# ตั้งค่าหน้าเว็บแบบ Warm Minimalist
st.set_page_config(
    page_title="CPU Scheduling Simulator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ฟังก์ชันตัวช่วยสำหรับ Render HTML โดยตัดช่องว่างนำหน้าทั้งหมด
# ป้องกันไม่ให้ Markdown Parser ตีความบรรทัดที่มีช่องว่างเป็น Code Block (<pre><code>)
def render_clean_html(html_str):
    compact_html = "".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(compact_html, unsafe_allow_html=True)


# ==============================================================================
# --- WARM MINIMALIST THEME STYLESHEET & PRINT CSS ---
# ==============================================================================
render_clean_html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Prompt', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1E293B;
    }
    
    /* 1. พื้นหลังสี Warm Cream นุ่ม ละมุนตา ไม่ขาวกระด้าง */
    .stApp {
        background-color: #FDFBF7 !important;
    }
    
    /* ซ่อน Header มาตรฐานของ Streamlit */
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* 2. สไตล์ปุ่ม Run Simulation: ขนาดพอดี ไม่ล้นจอ พร้อมเอฟเฟกต์ยกตัวเมื่อ Hover */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-family: 'Prompt', sans-serif !important;
        padding: 10px 28px !important;
        font-size: 15px !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.22) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
        box-shadow: 0 8px 22px rgba(79, 70, 229, 0.35) !important;
        transform: translateY(-2px) !important;
    }
    .stButton > button[kind="primary"]:active {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 6px rgba(79, 70, 229, 0.2) !important;
    }
    
    /* ปุ่ม Secondary */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-family: 'Prompt', sans-serif !important;
        padding: 8px 18px !important;
        font-size: 13.5px !important;
        transition: all 0.15s ease !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
        color: #334155 !important;
        box-shadow: 0 2px 6px rgba(149, 157, 165, 0.05) !important;
    }
    .stButton > button:hover {
        background-color: #F8FAFC !important;
        border-color: #CBD5E1 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(149, 157, 165, 0.1) !important;
    }
    .stButton > button:active {
        transform: translateY(1px) !important;
    }
    
    /* Input Fields */
    [data-testid="stNumberInput"] label, [data-testid="stSelectbox"] label, [data-testid="stRadio"] label {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
    }
    [data-testid="stNumberInput"] input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
    }
    
    /* สไตล์ Radio Switcher */
    div[data-testid="stRadio"] > div {
        gap: 16px;
    }
    
    /* ตาราง Data Editor */
    div[data-testid="stDataEditor"] {
        background-color: #FFFFFF !important;
        border: 1px solid #F1EFEA !important;
        border-radius: 14px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 24px rgba(149, 157, 165, 0.06) !important;
    }
    
    /* คลาสสำหรับเนื้อหาที่แสดงเฉพาะตอนสั่งพิมพ์ */
    .print-only {
        display: none;
    }
    
    /* ========================================================================== */
    /* --- PRINT CSS: จัดหน้ากระดาษ A4 สำหรับพิมพ์รายงาน / SAVE AS PDF --- */
    /* ========================================================================== */
    @media print {
        @page {
            size: A4 portrait;
            margin: 12mm 12mm 15mm 12mm;
        }
        
        /* 1. ซ่อนแถบเครื่องมือและเมนู Streamlit ทั้งหมด */
        header, 
        footer, 
        [data-testid="stHeader"], 
        [data-testid="stToolbar"], 
        [data-testid="stDecoration"], 
        [data-testid="stStatusWidget"],
        #MainMenu, 
        .stDeployButton,
        iframe,
        .no-print {
            display: none !important;
        }
        
        /* 2. ซ่อนปุ่มและคอนโทรลที่ไม่เกี่ยวกับการพิมพ์ */
        .stButton,
        button,
        [data-testid="stNumberInput"],
        [data-testid="stSelectbox"],
        div[data-testid="stRadio"],
        div[data-testid="stDataEditor"],
        .guidance-card {
            display: none !important;
        }
        
        /* 3. แสดงเนื้อหาเฉพาะตอนพิมพ์ */
        .print-only {
            display: block !important;
        }
        
        /* 4. บังคับพื้นหลังกระดาษขาว ตัวอักษรดำชัดเจน */
        html, body, .stApp, [class*="css"] {
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        
        * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
            color-adjust: exact !important;
        }
        
        /* 5. จัดระเบียบตารางและชาร์ตไม่ให้ขาดท่อนข้ามหน้า */
        table, tr, td, th, .gantt-outer-card, .metric-cards-container, .winner-card {
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }
        
        table {
            border-color: #CBD5E1 !important;
        }
        
        .gantt-scroll-container {
            overflow: visible !important;
        }
        
        .gantt-outer-card {
            box-shadow: none !important;
            border: 1px solid #CBD5E1 !important;
            margin-bottom: 20px !important;
        }
    }
    </style>
""")


# ==============================================================================
# --- HEADER BAR & WORKING JAVASCRIPT PRINT BUTTON ---
# ==============================================================================
col_head, col_btn = st.columns([3.6, 1.4])
with col_head:
    render_clean_html("""
        <div>
            <h1 style="font-size: 24px; font-weight: 700; color: #0F172A; margin: 0 0 4px 0; letter-spacing: -0.3px;">CPU Scheduling Simulator</h1>
            <p style="font-size: 13.5px; color: #64748B; margin: 0;">การจำลองการจัดตารางเวลาซีพียู: FCFS, SJF (Non-preemptive) และ Round Robin</p>
        </div>
    """)
with col_btn:
    # ปุ่มพิมพ์ด้วย JavaScript window.parent.print() ผ่าน components.html
    # เพื่อให้ทำงานได้จริงโดยตรงในเบราว์เซอร์
    components.html("""
        <div style="display: flex; justify-content: flex-end; align-items: flex-start; height: 100%; margin-top: 4px;">
            <button id="print-trigger-btn" onclick="executePrint()" style="
                background: #FFFFFF;
                color: #334155;
                border: 1px solid #CBD5E1;
                padding: 8px 18px;
                border-radius: 10px;
                font-size: 13.5px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 2px 6px rgba(149, 157, 165, 0.08);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Prompt', sans-serif;
                transition: all 0.15s ease;
                display: inline-flex;
                align-items: center;
                gap: 6px;
                white-space: nowrap;
            " onmouseover="this.style.background='#F8FAFC'; this.style.borderColor='#94A3B8'; this.style.transform='translateY(-1px)';"
               onmouseout="this.style.background='#FFFFFF'; this.style.borderColor='#CBD5E1'; this.style.transform='translateY(0)';"
               onmousedown="this.style.transform='translateY(1px)';">
                <span>🖨️ พิมพ์รายงาน / PDF</span>
            </button>
        </div>
        <script>
            function executePrint() {
                try {
                    if (window.parent && window.parent !== window) {
                        window.parent.print();
                    } else {
                        window.print();
                    }
                } catch (e) {
                    window.print();
                }
            }
        </script>
    """, height=48)


# ==============================================================================
# --- PASTEL COLOR PALETTE (P1 - P10) ---
# ==============================================================================
PASTEL_PALETTE = {
    "P1":  {"bg": "#FFD1BA", "border": "#FDBA74", "text": "#431407", "name": "Soft Peach"},
    "P2":  {"bg": "#DDD6FE", "border": "#C4B5FD", "text": "#3B0764", "name": "Lavender"},
    "P3":  {"bg": "#A7F3D0", "border": "#6EE7B7", "text": "#064E3B", "name": "Mint Green"},
    "P4":  {"bg": "#FEF08A", "border": "#FDE047", "text": "#713F12", "name": "Butter Yellow"},
    "P5":  {"bg": "#FBCFE8", "border": "#F472B6", "text": "#831843", "name": "Soft Pink"},
    "P6":  {"bg": "#BAE6FD", "border": "#7DD3FC", "text": "#0369A1", "name": "Sky Blue"},
    "P7":  {"bg": "#FED7AA", "border": "#FDBA74", "text": "#7C2D12", "name": "Warm Apricot"},
    "P8":  {"bg": "#D9F99D", "border": "#BEF264", "text": "#365314", "name": "Matcha Lime"},
    "P9":  {"bg": "#E9D5FF", "border": "#D8B4FE", "text": "#581C87", "name": "Lilac"},
    "P10": {"bg": "#C7D2FE", "border": "#A5B4FC", "text": "#312E81", "name": "Periwinkle"},
}

IDLE_STYLE = {
    "bg": "#F1F5F9",
    "border": "#CBD5E1",
    "text": "#64748B",
    "name": "Idle"
}

def get_process_style(p_name):
    if p_name == "Idle":
        return IDLE_STYLE
    if p_name in PASTEL_PALETTE:
        return PASTEL_PALETTE[p_name]
    palette_list = list(PASTEL_PALETTE.values())
    try:
        num = int(''.join(filter(str.isdigit, str(p_name))))
        return palette_list[(num - 1) % len(palette_list)]
    except Exception:
        return palette_list[abs(hash(str(p_name))) % len(palette_list)]


# ==============================================================================
# --- DATA GENERATOR (AT 0-3 ชิดกัน รับประกันว่าไม่มีช่องว่าง IDLE) ---
# ==============================================================================
SUBJECTS = [
    "แบบฝึกหัด OS", "รายงาน Database", "โครงงาน Network",
    "สรุป English", "แบบฝึกหัด Math", "เตรียมสอบ IT Security",
    "แล็บ Cloud Computing", "การบ้าน Data Structures",
    "เขียนโปรแกรม Web App", "ออกแบบ UX/UI", "วิจัย Machine Learning", "โครงงาน IoT"
]

def generate_data(seed, count):
    random.seed(seed)
    subj_pool = SUBJECTS.copy()
    random.shuffle(subj_pool)
    
    rows = []
    current_coverage = 0
    for i in range(count):
        bt = random.randint(2, 7)
        if i == 0:
            at = 0
        else:
            max_at = min(3, max(1, current_coverage))
            at = random.randint(0, max_at)
        current_coverage += bt
        
        subj = subj_pool[i % len(subj_pool)]
        rows.append({
            "Process": f"P{i+1}",
            "ชื่องาน / วิชา": subj,
            "AT": at,
            "BT": bt
        })
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

# กำหนดให้เริ่มต้นเป็น False (ยังไม่แสดงผลลัพธ์จนกว่าจะกดปุ่ม Run)
if "has_run" not in st.session_state:
    st.session_state.has_run = False

def on_random_click():
    current_seed = st.session_state.get("seed_val", 1234)
    new_seed = random.randint(1000, 9999)
    while new_seed == current_seed:
        new_seed = random.randint(1000, 9999)
    st.session_state.seed_val = new_seed
    st.session_state.prev_seed = new_seed
    st.session_state.random_key += 1
    st.session_state.process_list = generate_data(new_seed, st.session_state.num_processes)
    # รีเซ็ตเป็น False ทันทีที่สุ่มโจทย์ใหม่ เพื่อซ่อนผลลัพธ์เก่าจนกว่าจะกด Run อีกครั้ง
    st.session_state.has_run = False


# ==============================================================================
# --- SYSTEM CONFIGURATION CARD ---
# ==============================================================================
render_clean_html("""
    <div style="font-size: 15px; font-weight: 700; color: #1E293B; margin-bottom: 10px;">
        ⚙️ System Configuration
    </div>
""")

col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.2, 1.2])

with col1:
    seed_val = st.number_input("Seed:", step=1, key="seed_val")
with col2:
    quantum_val = st.number_input("Time Quantum (q):", min_value=1, max_value=8, value=2, step=1)
with col3:
    num_processes = st.selectbox(
        "Number of Processes:",
        options=list(range(3, 11)),
        index=list(range(3, 11)).index(st.session_state.num_processes) if st.session_state.num_processes in range(3, 11) else 2,
        key="num_processes"
    )
with col4:
    st.write("")
    st.write("")
    st.button("🎲 สุ่มโจทย์ใหม่", on_click=on_random_click, use_container_width=True)

# ตรวจสอบการเปลี่ยน Time Quantum
if "prev_quantum" not in st.session_state:
    st.session_state.prev_quantum = quantum_val
if st.session_state.prev_quantum != quantum_val:
    st.session_state.prev_quantum = quantum_val
    st.session_state.has_run = False

# ตรวจสอบการเปลี่ยนค่า Seed หรือจำนวนงาน
if st.session_state.prev_seed != seed_val:
    st.session_state.prev_seed = seed_val
    st.session_state.random_key += 1
    st.session_state.process_list = generate_data(seed_val, num_processes)
    st.session_state.has_run = False
elif st.session_state.prev_num_processes != num_processes or len(st.session_state.process_list) != num_processes:
    st.session_state.prev_num_processes = num_processes
    st.session_state.random_key += 1
    st.session_state.process_list = generate_data(seed_val, num_processes)
    st.session_state.has_run = False


# ==============================================================================
# --- PROCESS QUEUE TABLE ---
# ==============================================================================
render_clean_html("""
    <div style="font-size: 15px; font-weight: 700; color: #1E293B; margin-top: 18px; margin-bottom: 10px;">
        📋 Job Queue
    </div>
""")

df = pd.DataFrame(st.session_state.process_list)

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed",
    disabled=["Process"],
    key=f"editor_{st.session_state.random_key}"
)

# ตรวจสอบว่ามีการแก้ไขค่าตัวเลขในตารางหรือไม่
edited_records = edited_df.to_dict("records")
if edited_records != st.session_state.process_list:
    st.session_state.process_list = edited_records
    st.session_state.has_run = False

processes_input = st.session_state.process_list

# ตาราง Job Queue สำหรับแสดงผลเฉพาะเวลาสั่งพิมพ์ / PDF (คมชัดระดับเวกเตอร์ ไม่เจอปัญหาแคนวาสหาย)
print_queue_rows = []
for p in processes_input:
    st_info = get_process_style(p["Process"])
    row_html = f"""
        <tr style="border-bottom: 1px solid #CBD5E1;">
            <td style="padding: 8px 12px; text-align: center;">
                <span style="display: inline-block; padding: 2px 10px; border-radius: 6px; font-weight: 700; font-size: 12px; background: {st_info['bg']}; color: {st_info['text']}; border: 1px solid {st_info['border']};">
                    {p['Process']}
                </span>
            </td>
            <td style="padding: 8px 12px; color: #1E293B; font-weight: 600; font-size: 13px;">{p['ชื่องาน / วิชา']}</td>
            <td style="padding: 8px 12px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #1E293B;">{p['AT']}</td>
            <td style="padding: 8px 12px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #1E293B;">{p['BT']}</td>
        </tr>
    """
    print_queue_rows.append(row_html)

print_job_queue_html = f"""
    <div class="print-only" style="margin-bottom: 22px;">
        <div style="font-size: 13px; color: #475569; margin-bottom: 8px; font-weight: 600;">
            พารามิเตอร์การทดลอง: Time Quantum (q) = {quantum_val} | Seed = {seed_val} | จำนวน Process = {len(processes_input)} งาน
        </div>
        <table style="width: 100%; border-collapse: collapse; text-align: left; border: 1px solid #CBD5E1; border-radius: 8px; overflow: hidden;">
            <thead>
                <tr style="background: #F8FAFC; border-bottom: 1.5px solid #CBD5E1;">
                    <th style="padding: 9px 12px; text-align: center; color: #334155; font-size: 12px; font-weight: 700;">Process</th>
                    <th style="padding: 9px 12px; color: #334155; font-size: 12px; font-weight: 700;">ชื่องาน / วิชา</th>
                    <th style="padding: 9px 12px; text-align: center; color: #334155; font-size: 12px; font-weight: 700;">Arrival Time (AT)</th>
                    <th style="padding: 9px 12px; text-align: center; color: #334155; font-size: 12px; font-weight: 700;">Burst Time (BT)</th>
                </tr>
            </thead>
            <tbody>
                {''.join(print_queue_rows)}
            </tbody>
        </table>
    </div>
"""
render_clean_html(print_job_queue_html)

# ==============================================================================

# 1. FCFS
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

# 2. SJF (Non-preemptive)
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

# 3. Round Robin (RR)
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
# --- TEXTBOOK-STYLE GANTT CHART (WITH HOVER SCALE EFFECT) ---
# ==============================================================================
def render_gantt_chart(gantt):
    if not gantt:
        return ""
        
    total_time = gantt[-1]["end"]
    unit_scale = max(44, min(75, int(960 / max(total_time, 1))))
    
    blocks_html = []
    n = len(gantt)
    
    for i, block in enumerate(gantt):
        p_name = block["Process"]
        st_t = block["start"]
        en_t = block["end"]
        duration = en_t - st_t
        width = duration * unit_scale
        
        style = get_process_style(p_name)
        bg = style["bg"]
        text_color = style["text"]
        
        is_first = (i == 0)
        is_last = (i == n - 1)
        
        radius_css = ""
        if is_first and is_last:
            radius_css = "border-radius: 6px;"
        elif is_first:
            radius_css = "border-top-left-radius: 6px; border-bottom-left-radius: 6px;"
        elif is_last:
            radius_css = "border-top-right-radius: 6px; border-bottom-right-radius: 6px;"
            
        # ตัวกล่อง Process พร้อมเอฟเฟกต์ Hover Scale เบาๆ
        bar_box = f"""
            <div style="
                height: 46px;
                width: 100%;
                background: {bg};
                color: {text_color};
                border-top: 2px solid #334155;
                border-bottom: 2px solid #334155;
                border-left: 2px solid #334155;
                border-right: 2px solid #334155;
                {radius_css}
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 15px;
                font-family: 'Prompt', sans-serif;
                box-sizing: border-box;
                user-select: none;
                cursor: pointer;
                transition: transform 0.18s ease, box-shadow 0.18s ease;
            " onmouseover="this.style.transform='translateY(-2px) scale(1.02)'; this.style.boxShadow='0 6px 16px rgba(0,0,0,0.08)';"
               onmouseout="this.style.transform='translateY(0px) scale(1)'; this.style.boxShadow='none';">
                {p_name}
            </div>
        """
        
        # ตัวเลขเวลาเริ่มต้นที่รอยต่อซ้ายสุด
        first_tick = ""
        if is_first:
            first_tick = f"""
                <div style="position: absolute; left: 0px; top: 46px; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; pointer-events: none; z-index: 2;">
                    <div style="width: 2px; height: 8px; background: #334155;"></div>
                    <span style="font-size: 13px; font-weight: 700; color: #1E293B; margin-top: 2px; font-family: 'JetBrains Mono', Consolas, monospace;">{st_t}</span>
                </div>
            """
            
        # ตัวเลขเวลาสิ้นสุดที่รอยต่อขวาของแต่ละบล็อก
        end_tick = f"""
            <div style="position: absolute; right: 0px; top: 46px; transform: translateX(50%); display: flex; flex-direction: column; align-items: center; pointer-events: none; z-index: 2;">
                <div style="width: 2px; height: 8px; background: #334155;"></div>
                <span style="font-size: 13px; font-weight: 700; color: #1E293B; margin-top: 2px; font-family: 'JetBrains Mono', Consolas, monospace;">{en_t}</span>
            </div>
        """
        
        block_html = f"""
            <div style="flex-shrink: 0; width: {width}px; position: relative; box-sizing: border-box;">
                {bar_box}{first_tick}{end_tick}
            </div>
        """
        blocks_html.append(block_html)
        
    gantt_inner = "".join(blocks_html)
    
    chart_container = f"""
        <div style="background: #FFFFFF; border: 1px solid #F1EFEA; border-radius: 16px; padding: 18px 20px 32px 20px; box-shadow: 0 8px 24px rgba(149, 157, 165, 0.08); margin: 12px 0 20px 0;">
            <div style="overflow-x: auto; padding-bottom: 4px;">
                <div style="display: inline-flex; flex-direction: row; margin: 10px 24px 28px 24px; position: relative;">
                    {gantt_inner}
                </div>
            </div>
        </div>
    """
    return chart_container


# ==============================================================================
# --- RESULTS TABLE COMPONENT ---
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
            <tr style="border-bottom: 1px solid #F8FAFC; background: #FFFFFF;">
                <td style="padding: 10px 14px; text-align: center;">
                    <span style="display: inline-block; padding: 3px 12px; border-radius: 6px; font-weight: 700; font-family: 'Prompt', sans-serif; font-size: 13px; background: {st_info['bg']}; color: {st_info['text']}; border: 1px solid {st_info['border']};">
                        {p_id}
                    </span>
                </td>
                <td style="padding: 10px 14px; color: #334155; font-weight: 500; font-size: 13.5px;">{p['ชื่องาน / วิชา']}</td>
                <td style="padding: 10px 14px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13.5px; color: #475569;">{p['AT']}</td>
                <td style="padding: 10px 14px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13.5px; color: #475569;">{p['BT']}</td>
                <td style="padding: 10px 14px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13.5px; color: #0F172A; font-weight: 600;">{c}</td>
                <td style="padding: 10px 14px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13.5px; color: #4F46E5; font-weight: 600;">{t}</td>
                <td style="padding: 10px 14px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13.5px; color: #059669; font-weight: 600;">{w}</td>
            </tr>
        """
        rows_html.append(row_html)
        
    table_html = f"""
        <div style="background: #FFFFFF; border: 1px solid #F1EFEA; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 24px rgba(149, 157, 165, 0.08); margin: 14px 0 18px 0;">
            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                    <tr style="background: #FAF8F5; border-bottom: 1.5px solid #EBE7DF;">
                        <th style="padding: 11px 14px; text-align: center; color: #475569; font-size: 12.5px; font-weight: 600;">Process</th>
                        <th style="padding: 11px 14px; color: #475569; font-size: 12.5px; font-weight: 600;">ชื่องาน / วิชา</th>
                        <th style="padding: 11px 14px; text-align: center; color: #475569; font-size: 12.5px; font-weight: 600;">AT (มาถึง)</th>
                        <th style="padding: 11px 14px; text-align: center; color: #475569; font-size: 12.5px; font-weight: 600;">BT (เวลา)</th>
                        <th style="padding: 11px 14px; text-align: center; color: #475569; font-size: 12.5px; font-weight: 600;">CT (เสร็จที่)</th>
                        <th style="padding: 11px 14px; text-align: center; color: #475569; font-size: 12.5px; font-weight: 600;">TAT (CT - AT)</th>
                        <th style="padding: 11px 14px; text-align: center; color: #475569; font-size: 12.5px; font-weight: 600;">WT (TAT - BT)</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows_html)}
                </tbody>
            </table>
        </div>
    """
    avg_tat = tot_tat / len(procs)
    avg_wt = tot_wt / len(procs)
    return table_html, avg_tat, avg_wt


# ==============================================================================
# --- RENDER SINGLE ALGORITHM VIEW ---
# ==============================================================================
def render_algorithm_view(title, result_tuple, procs):
    gantt, res = result_tuple
    
    render_clean_html(f"""
        <div style="font-size: 16px; font-weight: 700; color: #0F172A; margin-top: 18px; margin-bottom: 6px;">
            {title}
        </div>
    """)
    
    # 1. Gantt Chart
    chart_html = render_gantt_chart(gantt)
    render_clean_html(chart_html)
    
    # 2. Table
    table_html, avg_tat, avg_wt = render_results_table(procs, res)
    render_clean_html(table_html)
    
    # 3. Metric Cards
    metric_cards_html = f"""
        <div style="display: flex; gap: 14px; margin: 14px 0 24px 0; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 200px; background: #FFFFFF; border: 1px solid #F1EFEA; border-left: 4px solid #6366F1; border-radius: 12px; padding: 14px 18px; box-shadow: 0 4px 14px rgba(149, 157, 165, 0.06);">
                <div style="font-size: 12px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 4px;">⏱️ Turnaround Time เฉลี่ย (Avg TAT)</div>
                <div style="font-size: 24px; font-weight: 700; color: #0F172A; font-family: 'JetBrains Mono', monospace;">
                    {avg_tat:.2f} <span style="font-size: 13px; font-weight: 400; color: #94A3B8; font-family: 'Prompt', sans-serif;">หน่วยเวลา</span>
                </div>
            </div>
            <div style="flex: 1; min-width: 200px; background: #FFFFFF; border: 1px solid #F1EFEA; border-left: 4px solid #10B981; border-radius: 12px; padding: 14px 18px; box-shadow: 0 4px 14px rgba(149, 157, 165, 0.06);">
                <div style="font-size: 12px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 4px;">⏳ Waiting Time เฉลี่ย (Avg WT)</div>
                <div style="font-size: 24px; font-weight: 700; color: #0F172A; font-family: 'JetBrains Mono', monospace;">
                    {avg_wt:.2f} <span style="font-size: 13px; font-weight: 400; color: #94A3B8; font-family: 'Prompt', sans-serif;">หน่วยเวลา</span>
                </div>
            </div>
        </div>
        <hr style="border: none; border-top: 1px solid #EBE7DF; margin: 24px 0;">
    """
    render_clean_html(metric_cards_html)
    return avg_tat, avg_wt


# ==============================================================================
# --- COMPARISON SUMMARY (WINNER CROWN + INTERACTIVE BAR CHART) ---
# ==============================================================================
def render_comparison_summary(r_fcfs, r_sjf, r_rr, q_val, procs):
    n = len(procs)
    
    # คำนวณ Avg TAT และ Avg WT
    tat_fcfs = sum(r_fcfs[1][p["Process"]]["TAT"] for p in procs) / n
    wt_fcfs = sum(r_fcfs[1][p["Process"]]["WT"] for p in procs) / n
    
    tat_sjf = sum(r_sjf[1][p["Process"]]["TAT"] for p in procs) / n
    wt_sjf = sum(r_sjf[1][p["Process"]]["WT"] for p in procs) / n
    
    tat_rr = sum(r_rr[1][p["Process"]]["TAT"] for p in procs) / n
    wt_rr = sum(r_rr[1][p["Process"]]["WT"] for p in procs) / n
    
    # หาผู้ชนะ (Avg WT น้อยที่สุด)
    candidates = [
        {"name": "SJF (Shortest Job First - Non-preemptive)", "short": "SJF", "wt": wt_sjf, "tat": tat_sjf},
        {"name": "FCFS (First-Come, First-Served)", "short": "FCFS", "wt": wt_fcfs, "tat": tat_fcfs},
        {"name": f"Round Robin (q = {q_val})", "short": "Round Robin", "wt": wt_rr, "tat": tat_rr},
    ]
    candidates.sort(key=lambda x: (x["wt"], x["tat"]))
    winner = candidates[0]
    
    # 1. การ์ดมงกุฎผู้ชนะ (Winner Crown Card)
    winner_card_html = f"""
        <div style="background: linear-gradient(135deg, #FFFDF5 0%, #FEF8E7 100%); border: 1.5px solid #FDE68A; border-radius: 16px; padding: 22px 26px; margin: 12px 0 24px 0; box-shadow: 0 8px 24px rgba(245, 158, 11, 0.08);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div style="font-size: 38px; line-height: 1; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">🏆</div>
                    <div>
                        <div style="font-size: 12.5px; font-weight: 700; color: #B45309; text-transform: uppercase; letter-spacing: 0.5px;">Best Performance Summary</div>
                        <div style="font-size: 21px; font-weight: 800; color: #78350F; margin-top: 2px;">
                            👑 ผู้ชนะ: {winner['short']} (Avg WT ต่ำสุด = {winner['wt']:.2f})
                        </div>
                        <div style="font-size: 13.5px; color: #92400E; margin-top: 4px;">
                            {winner['name']} ทำเวลารอคอยเฉลี่ยน้อยที่สุด มีประสิทธิภาพสูงสุดสำหรับชุดข้อมูลนี้
                        </div>
                    </div>
                </div>
                <div style="display: flex; gap: 12px;">
                    <div style="background: #FFFFFF; border: 1px solid #FCD34D; border-radius: 12px; padding: 10px 18px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                        <div style="font-size: 11.5px; font-weight: 600; color: #92400E;">Avg WT ต่ำที่สุด</div>
                        <div style="font-size: 22px; font-weight: 800; color: #B45309; font-family: 'JetBrains Mono', monospace;">{winner['wt']:.2f}</div>
                    </div>
                    <div style="background: #FFFFFF; border: 1px solid #FCD34D; border-radius: 12px; padding: 10px 18px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                        <div style="font-size: 11.5px; font-weight: 600; color: #92400E;">Avg TAT</div>
                        <div style="font-size: 22px; font-weight: 800; color: #4F46E5; font-family: 'JetBrains Mono', monospace;">{winner['tat']:.2f}</div>
                    </div>
                </div>
            </div>
        </div>
    """
    render_clean_html(winner_card_html)
    
    # 2. กราฟแท่งเปรียบเทียบ Interactive Bar Chart (Altair)
    render_clean_html("""
        <div style="font-size: 15px; font-weight: 700; color: #1E293B; margin-top: 20px; margin-bottom: 8px;">
            📊 กราฟเปรียบเทียบค่าเฉลี่ย (Average Metrics Comparison)
        </div>
    """)
    
    chart_data = pd.DataFrame([
        {"Algorithm": "FCFS", "Metric": "Avg Turnaround Time (TAT)", "Value": round(tat_fcfs, 2)},
        {"Algorithm": "FCFS", "Metric": "Avg Waiting Time (WT)", "Value": round(wt_fcfs, 2)},
        {"Algorithm": "SJF", "Metric": "Avg Turnaround Time (TAT)", "Value": round(tat_sjf, 2)},
        {"Algorithm": "SJF", "Metric": "Avg Waiting Time (WT)", "Value": round(wt_sjf, 2)},
        {"Algorithm": f"Round Robin (q={q_val})", "Metric": "Avg Turnaround Time (TAT)", "Value": round(tat_rr, 2)},
        {"Algorithm": f"Round Robin (q={q_val})", "Metric": "Avg Waiting Time (WT)", "Value": round(wt_rr, 2)},
    ])
    
    bar_chart = (
        alt.Chart(chart_data)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("Algorithm:N", title=None, axis=alt.Axis(labelAngle=0, labelFont='Prompt', labelFontSize=13, labelColor='#334155')),
            y=alt.Y("Value:Q", title="หน่วยเวลา (Time Units)", axis=alt.Axis(labelFont='Prompt', titleFont='Prompt', labelColor='#64748B')),
            color=alt.Color(
                "Metric:N",
                scale=alt.Scale(
                    domain=["Avg Turnaround Time (TAT)", "Avg Waiting Time (WT)"],
                    range=["#818CF8", "#34D399"]
                ),
                legend=alt.Legend(title=None, orient="top", labelFont='Prompt', labelFontSize=13)
            ),
            xOffset="Metric:N",
            tooltip=[
                alt.Tooltip("Algorithm:N", title="Algorithm"),
                alt.Tooltip("Metric:N", title="Metric"),
                alt.Tooltip("Value:Q", title="Value (หน่วยเวลา)")
            ]
        )
        .properties(height=340)
        .configure_view(strokeWidth=0)
    )
    st.altair_chart(bar_chart, use_container_width=True)
    
    # 3. ตารางสรุปเปรียบเทียบแบบเคียงข้างกัน (Comparison Table)
    render_clean_html("""
        <div style="font-size: 15px; font-weight: 700; color: #1E293B; margin-top: 24px; margin-bottom: 8px;">
            📑 ตารางเปรียบเทียบค่าสถิติทั้ง 3 อัลกอริทึม
        </div>
    """)
    
    # จัดลำดับ Rank
    rank_badges = {"0": "🥇 ยอดเยี่ยม (อันดับ 1)", "1": "🥈 อันดับ 2", "2": "🥉 อันดับ 3"}
    summary_rows = []
    for idx, c in enumerate(candidates):
        rank_label = rank_badges.get(str(idx), "")
        row_bg = "background: #FFFDF5;" if idx == 0 else "background: #FFFFFF;"
        row_html = f"""
            <tr style="border-bottom: 1px solid #F1EFEA; {row_bg}">
                <td style="padding: 12px 16px; font-weight: 700; color: #0F172A; font-size: 13.5px;">{c['name']}</td>
                <td style="padding: 12px 16px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 14px; color: #4F46E5; font-weight: 700;">{c['tat']:.2f}</td>
                <td style="padding: 12px 16px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 14px; color: #059669; font-weight: 700;">{c['wt']:.2f}</td>
                <td style="padding: 12px 16px; text-align: center;">
                    <span style="display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; background: {'#FEF3C7' if idx==0 else '#F1F5F9'}; color: {'#92400E' if idx==0 else '#475569'}; border: 1px solid {'#FDE68A' if idx==0 else '#E2E8F0'};">
                        {rank_label}
                    </span>
                </td>
            </tr>
        """
        summary_rows.append(row_html)
        
    comp_table_html = f"""
        <div style="background: #FFFFFF; border: 1px solid #F1EFEA; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 24px rgba(149, 157, 165, 0.08); margin: 12px 0 24px 0;">
            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                    <tr style="background: #FAF8F5; border-bottom: 1.5px solid #EBE7DF;">
                        <th style="padding: 12px 16px; color: #475569; font-size: 13px; font-weight: 600;">Algorithm</th>
                        <th style="padding: 12px 16px; text-align: center; color: #475569; font-size: 13px; font-weight: 600;">Avg Turnaround Time (TAT)</th>
                        <th style="padding: 12px 16px; text-align: center; color: #475569; font-size: 13px; font-weight: 600;">Avg Waiting Time (WT)</th>
                        <th style="padding: 12px 16px; text-align: center; color: #475569; font-size: 13px; font-weight: 600;">สรุปผลประเมิน</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(summary_rows)}
                </tbody>
            </table>
        </div>
    """
    render_clean_html(comp_table_html)


# ==============================================================================
# --- SIMULATION EXECUTION TRIGGER & VIEW SWITCHER ---
# ==============================================================================
render_clean_html("<div style='height: 16px;'></div>")

# ปรับปุ่ม Run Simulation ให้ขนาดสวยงาม อยู่ตรงกลาง ไม่ยาวล้นจอ
col_btn_l, col_btn_c, col_btn_r = st.columns([1, 1.4, 1])
with col_btn_c:
    if st.button("🚀 คำนวณตารางงาน (Run Simulation)", type="primary", use_container_width=True):
        st.session_state.has_run = True

render_clean_html("<div style='height: 16px;'></div>")

# ทำการคำนวณผลลัพธ์
if st.session_state.get("has_run", False):
    r_fcfs = run_fcfs(processes_input)
    r_sjf = run_sjf(processes_input)
    r_rr = run_rr(processes_input, quantum_val)
    
    # 2. ตัวเลือกระบบมุมมอง (View Mode Switcher)
    col_view_title, col_view_radio = st.columns([1.2, 2.8])
    with col_view_title:
        render_clean_html("""
            <div style="font-size: 16px; font-weight: 700; color: #0F172A; padding-top: 8px;">
                🖥️ รูปแบบมุมมอง (View Mode):
            </div>
        """)
    with col_view_radio:
        view_mode = st.radio(
            "View Mode:",
            options=["📑 Tabs View (แยกตามอัลกอริทึม)", "📜 Scroll View (แสดงยาวในหน้าเดียว)"],
            horizontal=True,
            label_visibility="collapsed"
        )
    
    render_clean_html("<div style='height: 10px;'></div>")
    
    if "Tabs View" in view_mode:
        tab_fcfs, tab_sjf, tab_rr, tab_comp = st.tabs([
            "FCFS", 
            "SJF (Non-preemptive)", 
            f"Round Robin (q = {quantum_val})", 
            "🏆 Comparison Summary"
        ])
        with tab_fcfs:
            render_algorithm_view("FCFS Scheduling", r_fcfs, processes_input)
        with tab_sjf:
            render_algorithm_view("SJF Scheduling (Non-preemptive)", r_sjf, processes_input)
        with tab_rr:
            render_algorithm_view(f"Round Robin Scheduling (q = {quantum_val})", r_rr, processes_input)
        with tab_comp:
            render_comparison_summary(r_fcfs, r_sjf, r_rr, quantum_val, processes_input)
    else:
        render_algorithm_view("FCFS Scheduling", r_fcfs, processes_input)
        render_algorithm_view("SJF Scheduling (Non-preemptive)", r_sjf, processes_input)
        render_algorithm_view(f"Round Robin Scheduling (q = {quantum_val})", r_rr, processes_input)
        render_clean_html("<div style='font-size: 18px; font-weight: 700; color: #0F172A; margin: 32px 0 12px 0;'>🏆 Comparison Summary</div>")
        render_comparison_summary(r_fcfs, r_sjf, r_rr, quantum_val, processes_input)
else:
    # การ์ดสถานะ / ข้อความแนะนำน่ารักๆ ระหว่างรอการกดคำนวณ
    render_clean_html("""
        <div style="background: #FFFFFF; border: 1.5px dashed #CBD5E1; border-radius: 16px; padding: 42px 28px; text-align: center; margin: 18px 0 32px 0; box-shadow: 0 4px 18px rgba(149, 157, 165, 0.05);">
            <div style="font-size: 38px; margin-bottom: 12px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.06));">✨</div>
            <div style="font-size: 17px; font-weight: 700; color: #0F172A; margin-bottom: 6px;">
                พร้อมจำลองการจัดตารางเวลาซีพียูแล้ว
            </div>
            <div style="font-size: 13.5px; color: #64748B; max-width: 520px; margin: 0 auto; line-height: 1.6;">
                ปรับแต่งค่าในตาราง Job Queue ด้านบน หรือสุ่มโจทย์ใหม่ตามต้องการ <br>
                จากนั้นกดปุ่ม <span style="display: inline-block; background: #EEF2FF; color: #4F46E5; font-weight: 600; padding: 2px 10px; border-radius: 6px; font-size: 13px;">🚀 คำนวณตารางงาน (Run Simulation)</span> ด้านบนเพื่อแสดงผลลัพธ์ Gantt Chart และสถิติเปรียบเทียบ
            </div>
        </div>
    """)
