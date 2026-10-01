def run_fcfs(processes):
    procs = sorted(processes, key=lambda x: (x['arrival'], x['id']))
    current_time = 0
    order = []
    results = []

    for p in procs:
        p_data = dict(p)
        if current_time < p_data['arrival']:
            current_time = p_data['arrival']
        finish_time = current_time + p_data['burst']
        turnaround = finish_time - p_data['arrival']
        waiting = turnaround - p_data['burst']

        p_data['finish'] = finish_time
        p_data['turnaround'] = turnaround
        p_data['waiting'] = waiting
        results.append(p_data)
        order.append(p_data['name'])
        current_time = finish_time

    return results, order


def run_sjf_non_preemptive(processes):
    ready_pool = [dict(p) for p in processes]
    current_time = 0
    order = []
    results = []

    while ready_pool:
        available = [p for p in ready_pool if p['arrival'] <= current_time]

        if not available:
            next_arrival = min(p['arrival'] for p in ready_pool)
            current_time = next_arrival
            continue

        # เลือกงานที่ Burst Time น้อยสุด ถ้าเท่ากันเลือกคนที่มาก่อน
        chosen = min(available, key=lambda x: (x['burst'], x['arrival']))
        ready_pool.remove(chosen)

        finish_time = current_time + chosen['burst']
        turnaround = finish_time - chosen['arrival']
        waiting = turnaround - chosen['burst']

        chosen['finish'] = finish_time
        chosen['turnaround'] = turnaround
        chosen['waiting'] = waiting

        results.append(chosen)
        order.append(chosen['name'])
        current_time = finish_time

    return results, order


def print_table(mode_name, results, order, note=""):
    print(f"\nMode: {mode_name}")
    print(f"Process Execution Order: {' -> '.join(order)}")
    if note:
        print(f"({note})")

    print(f"{'Process':<9}{'Arrival':<9}{'Burst':<8}{'Finish':<8}{'Turnaround':<12}{'Waiting':<8}")
    for p in results:
        print(f"{p['name']:<9}{p['arrival']:<9}{p['burst']:<8}{p['finish']:<8}{p['turnaround']:<12}{p['waiting']:<8}")

    avg_turnaround = sum(p['turnaround'] for p in results) / len(results)
    avg_waiting = sum(p['waiting'] for p in results) / len(results)

    tag = "FCFS" if "FCFS" in mode_name else "SJF"
    print(f"\n[{tag} Summary]")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Waiting Time: {avg_waiting:.2f}")


def main():
    print("CPU SCHEDULING SIMULATOR (FCFS & SJF)")
    n = int(input("Enter number of processes: "))
    processes = []

    for i in range(1, n + 1):
        print(f"Enter details for Process {i}:")
        arrival = int(input("- Arrival Time: "))
        burst = int(input("- Burst Time: "))
        processes.append({'id': i, 'name': f"P{i}", 'arrival': arrival, 'burst': burst})

    input("\n[Data entered successfully! Press Enter to calculate...]")

    fcfs_results, fcfs_order = run_fcfs(processes)
    print_table("First-Come First-Served (FCFS)", fcfs_results, fcfs_order)

    sjf_results, sjf_order = run_sjf_non_preemptive(processes)
    print_table("Shortest Job First (SJF) - Non Preemptive", sjf_results, sjf_order,
                note="Note: P1 runs first. Then P4 is shortest among waiting processes")


if __name__ == "__main__":
    main()
     