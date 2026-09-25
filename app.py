import streamlit as st
import random
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="CPU Scheduling Simulation", layout="wide")
st.title("เว็บการจัดตารางงานส่วนบุคคล (CPU Scheduling)")

# เพิ่มปุ่มพิมพ์รายงาน (Print / Save as PDF)
st.markdown("""
    <div style="text-align: right; margin-bottom: 10px;">
        <button onclick="window.print()" style="padding: 6px 14px; background-color: #2c3e50; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
             พิมพ์รายงาน / บันทึกเป็น PDF
        </button>
    </div>
""", unsafe_allow_html=True)

# รายชื่อวิชาสำหรับการสุ่ม
SUBJECTS = [
    "แบบฝึกหัด OS", "รายงาน Database", "โครงงาน Network",
    "สรุป English", "แบบฝึกหัด Math", "เตรียมสอบ IT Security"
]

# --- 1. แผงควบคุมการสุ่มและรับค่า ---
st.subheader("1. กำหนดค่าเริ่มต้นและสุ่มโจทย์")
col1, col2, col3, col4 = st.columns(4)

with col1:
    seed_val = st.number_input("ค่า Seed:", value=1234, step=1)
with col2:
    quantum_val = st.number_input("Time Quantum (q = 1-4):", min_value=1, max_value=4, value=2, step=1)
with col3:
    num_processes = st.selectbox("จำนวนงาน:", [5, 6], index=0)
with col4:
    st.write("")
    btn_random = st.button("สุ่มโจทย์ใหม่")

# ฟังก์ชันสุ่มโจทย์
def generate_data(seed, count):
    random.seed(seed)
    zero_idx = random.randint(0, count - 1)
    rows = []
    for i in range(count):
        at = 0 if i == zero_idx else random.randint(0, 10)
        bt = random.randint(1, 8)
        rows.append({
            "Process": f"P{i+1}",
            "ชื่องาน / วิชา": random.choice(SUBJECTS),
            "AT": at,
            "BT": bt
        })
    return rows

if "process_list" not in st.session_state or btn_random:
    st.session_state.process_list = generate_data(seed_val, num_processes)

# --- 2. แสดงตารางที่แก้ไขค่าได้เอง ---
st.subheader("2. รายการงาน (ดับเบิลคลิกที่ช่องเพื่อแก้ไขค่าได้)")
df = pd.DataFrame(st.session_state.process_list)

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed",
    disabled=["Process"]
)
st.session_state.process_list = edited_df.to_dict("records")
processes_input = st.session_state.process_list


# ==========================================
# --- 3. ฟังก์ชันคำนวณ Scheduling 3 แบบ ---
# ==========================================

# 3.1 FCFS
def run_fcfs(procs):
    p_sorted = sorted(procs, key=lambda x: (x["AT"], int(x["Process"][1:])))
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
    rem_procs = [{**p, "p_num": int(p["Process"][1:])} for p in procs]
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
    p_data = [{**p, "rem_bt": p["BT"], "p_num": int(p["Process"][1:])} for p in procs]
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


# ==========================================
# --- 4. ฟังก์ชันวาดผลลัพธ์และ Gantt Chart ---
# ==========================================
def display_results(title, gantt, res, procs):
    st.subheader(f"ผลลัพธ์: {title}")
    
    # วาด Gantt Chart (เขียน HTML แบบบรรทัดเดียวชิดกันเพื่อป้องกัน Streamlit แสดงผลโค้ดหลุด)
    blocks_html = []
    for block in gantt:
        duration = block["end"] - block["start"]
        width = max(duration * 50, 60)
        is_idle = block["Process"] == "Idle"
        bg_color = "#7f8c8d" if is_idle else "#2980b9"
        
        b_html = (
            f'<div style="flex-shrink: 0; width: {width}px; background: {bg_color}; color: white; '
            f'border: 1px solid white; text-align: center; border-radius: 4px; margin-right: 2px;">'
            f'<div style="font-weight: bold; font-size: 14px; padding: 6px 0;">{block["Process"]}</div>'
            f'<div style="font-size: 11px; background: rgba(0,0,0,0.25); padding: 2px 0;">{block["start"]} - {block["end"]}</div>'
            f'</div>'
        )
        blocks_html.append(b_html)
        
    chart_container = (
        '<div style="display: flex; flex-direction: row; align-items: center; overflow-x: auto; '
        'background: #ecf0f1; padding: 12px; border-radius: 8px; margin-bottom: 15px;">'
        + "".join(blocks_html) + 
        '</div>'
    )
    st.markdown(chart_container, unsafe_allow_html=True)
    
    # ตารางสรุปค่า
    table_rows = []
    tot_tat = 0
    tot_wt = 0
    for p in procs:
        p_id = p["Process"]
        c = res[p_id]["CT"]
        t = res[p_id]["TAT"]
        w = res[p_id]["WT"]
        tot_tat += t
        tot_wt += w
        table_rows.append({
            "Process": p_id,
            "ชื่องาน": p["ชื่องาน / วิชา"],
            "AT": p["AT"],
            "BT": p["BT"],
            "CT (เสร็จที่)": c,
            "TAT (CT-AT)": t,
            "WT (TAT-BT)": w
        })
    
    res_df = pd.DataFrame(table_rows)
    st.dataframe(res_df, use_container_width=True, hide_index=True)
    
    avg_tat = tot_tat / len(procs)
    avg_wt = tot_wt / len(procs)
    c1, c2 = st.columns(2)
    c1.metric("Turnaround Time เฉลี่ย (Avg TAT)", f"{avg_tat:.2f}")
    c2.metric("Waiting Time เฉลี่ย (Avg WT)", f"{avg_wt:.2f}")
    st.divider()


# ==========================================
# --- 5. ปุ่มกดคำนวณและแสดงผลเปรียบเทียบ ---
# ==========================================
st.subheader("3. การประมวลผลตารางงาน")
if st.button(" คำนวณเปรียบเทียบทั้ง 3 อัลกอริทึม", type="primary"):
    g_fcfs, r_fcfs = run_fcfs(processes_input)
    display_results("FCFS (First-Come, First-Served)", g_fcfs, r_fcfs, processes_input)
    
    g_sjf, r_sjf = run_sjf(processes_input)
    display_results("SJF (Shortest Job First - Non-preemptive)", g_sjf, r_sjf, processes_input)
    
    g_rr, r_rr = run_rr(processes_input, quantum_val)
    display_results(f"Round Robin (Time Quantum = {quantum_val})", g_rr, r_rr, processes_input)