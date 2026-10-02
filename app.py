import streamlit as st
import random
import pandas as pd

# ตั้งค่าหน้าเว็บแบบ Light Minimalist
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
# --- LIGHT MINIMALIST PASTEL STYLESHEET ---
# ==============================================================================
render_clean_html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Prompt', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1E293B;
    }
    
    /* พื้นหลังสีสว่าง คลีน มินิมอล */
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    /* ซ่อน Header มาตรฐานของ Streamlit */
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* ปุ่มกดหลักและรองแบบเรียบหรู */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'Prompt', sans-serif !important;
        padding: 8px 18px !important;
        font-size: 14px !important;
        transition: all 0.15s ease !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
        color: #334155 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
    }
    .stButton > button:hover {
        background-color: #F1F5F9 !important;
        border-color: #94A3B8 !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(1px) !important;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 1px 3px rgba(79, 70, 229, 0.25) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #4338CA !important;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.35) !important;
    }
    
    /* Input Fields */
    [data-testid="stNumberInput"] label, [data-testid="stSelectbox"] label {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
    }
    [data-testid="stNumberInput"] input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    
    /* ตาราง Data Editor */
    div[data-testid="stDataEditor"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
    }
    
    /* Print Layout */
    @media print {
        header, footer, .stButton, [data-testid="stToolbar"] {
            display: none !important;
        }
        .stApp {
            background: #FFFFFF !important;
        }
    }
    </style>
""")


# ==============================================================================
# --- HEADER BAR ---
# ==============================================================================
render_clean_html("""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #E2E8F0;">
        <div>
            <h1 style="font-size: 24px; font-weight: 700; color: #0F172A; margin: 0 0 4px 0; letter-spacing: -0.3px;">CPU Scheduling Simulator</h1>
            <p style="font-size: 13.5px; color: #64748B; margin: 0;">การจำลองการจัดตารางเวลาซีพียู: FCFS, SJF (Non-preemptive) และ Round Robin</p>
        </div>
        <div>
            <button onclick="window.print()" style="
                background: #FFFFFF;
                color: #334155;
                border: 1px solid #CBD5E1;
                padding: 7px 16px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 1px 2px rgba(0,0,0,0.04);
                font-family: 'Prompt', sans-serif;
            ">
                🖨️ พิมพ์รายงาน / PDF
            </button>
        </div>
    </div>
""")


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
    # กำหนดให้ Process แรกมี AT = 0 เสมอ
    # และ Process ถัดไปมี AT อยู่ในช่วง 0 ถึง 3 อย่างต่อเนื่อง เพื่อไม่ให้เกิด Idle คั่นกลาง
    current_coverage = 0
    for i in range(count):
        bt = random.randint(2, 7)
        if i == 0:
            at = 0
        else:
            # สุ่ม AT ในช่วง 0 ถึง 3 และไม่เกิน cumulative burst time ที่มี เพื่อให้งานพร้อมรันต่อเนื่อง
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

if st.session_state.prev_seed != seed_val:
    st.session_state.prev_seed = seed_val
    st.session_state.random_key += 1
    st.session_state.process_list = generate_data(seed_val, num_processes)
elif st.session_state.prev_num_processes != num_processes or len(st.session_state.process_list) != num_processes:
    st.session_state.prev_num_processes = num_processes
    st.session_state.random_key += 1
    st.session_state.process_list = generate_data(seed_val, num_processes)


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
st.session_state.process_list = edited_df.to_dict("records")
processes_input = st.session_state.process_list


# ==============================================================================
# --- SCHEDULING ALGORITHMS (FCFS, SJF-NP, ROUND ROBIN) ---
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
# --- TEXTBOOK-STYLE CLEAN GANTT CHART ---
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
        
        # กรอบแบบเรียน: เส้นขอบเข้มต่อเนื่องชัดเจน
        radius_css = ""
        if is_first and is_last:
            radius_css = "border-radius: 6px;"
        elif is_first:
            radius_css = "border-top-left-radius: 6px; border-bottom-left-radius: 6px;"
        elif is_last:
            radius_css = "border-top-right-radius: 6px; border-bottom-right-radius: 6px;"
            
        # ตัวกล่องแสดงเฉพาะรหัส Process ตรงกลางเท่านั้น
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
            ">
                {p_name}
            </div>
        """
        
        # ตัวเลขเวลาที่รอยต่อด้านล่าง: จุดเริ่มต้นที่บล็อกแรกสุด
        first_tick = ""
        if is_first:
            first_tick = f"""
                <div style="position: absolute; left: 0px; top: 46px; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; pointer-events: none; z-index: 2;">
                    <div style="width: 2px; height: 8px; background: #334155;"></div>
                    <span style="font-size: 13px; font-weight: 700; color: #1E293B; margin-top: 2px; font-family: 'JetBrains Mono', Consolas, monospace;">{st_t}</span>
                </div>
            """
            
        # ตัวเลขเวลาที่รอยต่อด้านขวาของแต่ละบล็อก
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
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px 20px 32px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); margin: 12px 0 20px 0;">
            <div style="overflow-x: auto; padding-bottom: 4px;">
                <div style="display: inline-flex; flex-direction: row; margin: 10px 24px 28px 24px; position: relative;">
                    {gantt_inner}
                </div>
            </div>
        </div>
    """
    return chart_container


# ==============================================================================
# --- CLEAN RESULTS TABLE & METRICS ---
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
            <tr style="border-bottom: 1px solid #F1F5F9; background: #FFFFFF;">
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
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.03); margin: 14px 0 18px 0;">
            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                    <tr style="background: #F8FAFC; border-bottom: 1.5px solid #E2E8F0;">
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
    return table_html, tot_tat, tot_wt

def display_results(title, result_tuple, procs):
    gantt, res = result_tuple
    
    render_clean_html(f"""
        <div style="font-size: 16px; font-weight: 700; color: #0F172A; margin-top: 24px; margin-bottom: 6px;">
            {title}
        </div>
    """)
    
    # 1. Gantt Chart แบบเรียน คลีน มินิมอล
    chart_html = render_gantt_chart(gantt)
    render_clean_html(chart_html)
    
    # 2. ตารางผลลัพธ์
    table_html, tot_tat, tot_wt = render_results_table(procs, res)
    render_clean_html(table_html)
    
    # 3. ค่าเฉลี่ยสไตล์การ์ดมินิมอล
    avg_tat = tot_tat / len(procs)
    avg_wt = tot_wt / len(procs)
    
    metric_cards_html = f"""
        <div style="display: flex; gap: 14px; margin: 14px 0 24px 0; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 200px; background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #4F46E5; border-radius: 10px; padding: 14px 18px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                <div style="font-size: 12px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 4px;">⏱️ Turnaround Time เฉลี่ย (Avg TAT)</div>
                <div style="font-size: 24px; font-weight: 700; color: #0F172A; font-family: 'JetBrains Mono', monospace;">
                    {avg_tat:.2f} <span style="font-size: 13px; font-weight: 400; color: #94A3B8; font-family: 'Prompt', sans-serif;">หน่วยเวลา</span>
                </div>
            </div>
            <div style="flex: 1; min-width: 200px; background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #059669; border-radius: 10px; padding: 14px 18px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                <div style="font-size: 12px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 4px;">⏳ Waiting Time เฉลี่ย (Avg WT)</div>
                <div style="font-size: 24px; font-weight: 700; color: #0F172A; font-family: 'JetBrains Mono', monospace;">
                    {avg_wt:.2f} <span style="font-size: 13px; font-weight: 400; color: #94A3B8; font-family: 'Prompt', sans-serif;">หน่วยเวลา</span>
                </div>
            </div>
        </div>
        <hr style="border: none; border-top: 1px solid #E2E8F0; margin: 24px 0;">
    """
    render_clean_html(metric_cards_html)


# ==============================================================================
# --- SIMULATION EXECUTION TRIGGER ---
# ==============================================================================
render_clean_html("<div style='height: 12px;'></div>")

if st.button("🚀 คำนวณตารางงาน (Run Simulation)", type="primary", use_container_width=True):
    display_results("FCFS Scheduling", run_fcfs(processes_input), processes_input)
    display_results("SJF Scheduling (Non-preemptive)", run_sjf(processes_input), processes_input)
    display_results(f"Round Robin Scheduling (q = {quantum_val})", run_rr(processes_input, quantum_val), processes_input)
