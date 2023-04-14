from RoundRobin import *
from MostFitTask import *
from VirtualMachine import *
from Task import *
from Pipeline import *
import csv


def create_pipelines():
    # region Declaring tasks for pipelines
    # Tasks for pipeline1
    p1_task1 = Task(180, sequential_flow=1, description="Process finance data")
    p1_task2 = Task(20.9, sequential_flow=1, description="Process finance data")

    p1_task3 = Task(15.8, sequential_flow=2, description="P&L x Transaction Lines")
    p1_task4 = Task(22.1, sequential_flow=2, description="B/S x Transaction Lines")
    p1_task5 = Task(4.7, sequential_flow=2, description="GL Account")
    p1_task6 = Task(8.3, sequential_flow=2, description="Budget Cost Center")

    p1_task7 = Task(0.8, sequential_flow=3, description="postings")
    p1_task8 = Task(3.2, sequential_flow=3, description="transaction_lines")
    p1_task9 = Task(0.1, sequential_flow=3, description="accounts")

    p1_task10 = Task(13.8, sequential_flow=4, description="Transaction Lines (Postings)")
    p1_task11 = Task(31.1, sequential_flow=4, description="Transaction Lines (Postings)")
    p1_task12 = Task(4.4, sequential_flow=4, description="Transaction Lines (Postings)")
    p1_task13 = Task(15.9, sequential_flow=4, description="Transaction Lines (Postings)")
    p1_task14 = Task(4.7, sequential_flow=4, description="Transaction Lines (Postings)")

    p1_task15 = Task(0.8, sequential_flow=5, description="Create cluster table")
    p1_task16 = Task(1.0, sequential_flow=5, description="Create cluster table")
    p1_task17 = Task(4.9, sequential_flow=5, description="Create cluster table")
    p1_task18 = Task(8.6, sequential_flow=5, description="Create cluster table")
    p1_task19 = Task(15.1, sequential_flow=5, description="Create cluster table")
    p1_task20 = Task(0.1, sequential_flow=5, description="Create cluster table")

    p1_task21 = Task(0.6, sequential_flow=6, description="Analyze tables")

    # Tasks for pipeline2
    p2_task22 = Task(0.1, sequential_flow=1, description="Clear cache")

    p2_task23 = Task(33.5, sequential_flow=2, description="Run data set compressions")

    p2_task24 = Task(1.0, sequential_flow=3, description="Fill data set models cache")

    # Tasks for pipeline3
    p3_task25 = Task(12, sequential_flow=1, description="Clear cache")

    p3_task26 = Task(24, sequential_flow=2, description="Run data set compressions")
    p3_task27 = Task(12, sequential_flow=2, description="Run data set compressions")

    p3_task28 = Task(5.0, sequential_flow=3, description="Fill data set models cache")

    # Tasks for pipeline4
    p4_task29 = Task(115, sequential_flow=1, description="Process finance data")
    p4_task30 = Task(30.9, sequential_flow=1, description="Process finance data")

    p4_task31 = Task(17.5, sequential_flow=2, description="P&L x Transaction Lines")
    p4_task32 = Task(21.3, sequential_flow=2, description="B/S x Transaction Lines")
    p4_task33 = Task(5.2, sequential_flow=2, description="GL Account")
    p4_task34 = Task(7.9, sequential_flow=2, description="Budget Cost Center")

    p4_task35 = Task(1.1, sequential_flow=3, description="postings")
    p4_task36 = Task(2.6, sequential_flow=3, description="transaction_lines")
    p4_task37 = Task(0.2, sequential_flow=3, description="accounts")

    p4_task38 = Task(12.9, sequential_flow=4, description="Transaction Lines (Postings)")
    p4_task39 = Task(27.4, sequential_flow=4, description="Transaction Lines (Postings)")
    p4_task40 = Task(6.3, sequential_flow=4, description="Transaction Lines (Postings)")
    p4_task41 = Task(17.4, sequential_flow=4, description="Transaction Lines (Postings)")
    p4_task42 = Task(4.2, sequential_flow=4, description="Transaction Lines (Postings)")

    p4_task43 = Task(0.4, sequential_flow=5, description="Create cluster table")
    p4_task44 = Task(1.6, sequential_flow=5, description="Create cluster table")
    p4_task45 = Task(4.2, sequential_flow=5, description="Create cluster table")
    p4_task46 = Task(6.4, sequential_flow=5, description="Create cluster table")
    p4_task47 = Task(17.2, sequential_flow=5, description="Create cluster table")
    p4_task48 = Task(0.4, sequential_flow=5, description="Create cluster table")

    p4_task49 = Task(0.55, sequential_flow=6, description="Analyze tables")

    # endregion

    p1_tasks = [p1_task1, p1_task2, p1_task3, p1_task4, p1_task5, p1_task6, p1_task7, p1_task8, p1_task9,
                p1_task10, p1_task11, p1_task12, p1_task13, p1_task14, p1_task15, p1_task16, p1_task17, p1_task18,
                p1_task19, p1_task20, p1_task21]
    pipeline1 = Pipeline(p1_tasks, "Process finance data")

    p2_tasks = [p2_task22, p2_task23, p2_task24]
    pipeline2 = Pipeline(p2_tasks, "Run data set compression")

    p3_tasks = [p3_task25, p3_task26, p3_task27, p3_task28]
    pipeline3 = Pipeline(p3_tasks, "Run data set compression")

    p4_tasks = [p4_task29, p4_task30, p4_task31, p4_task32, p4_task33, p4_task34, p4_task35, p4_task36, p4_task37,
                p4_task38, p4_task39, p4_task40, p4_task41, p4_task42, p4_task43, p4_task44, p4_task45, p4_task46,
                p4_task47, p4_task48, p4_task49]
    pipeline4 = Pipeline(p4_tasks, "Process finance data")

    pipelines = [pipeline1, pipeline2, pipeline3, pipeline4]

    return pipelines


def create_VMs():
    m1 = VirtualMachine(clock_speed=3.2)
    m2 = VirtualMachine(clock_speed=4.1)
    m3 = VirtualMachine(clock_speed=5.7)
    machines = [m1, m2, m3]

    return machines


def execute_Round_Robin():
    pipelines = create_pipelines()
    machines = create_VMs()

    # region Execution of Round Robin
    time_quantum = 10

    RR = RoundRobin(machines, pipelines, time_quantum)
    # RR.execute_RR()
    result = RR.execute_RR_better()
    with open("./results_RR.csv", "a", newline="") as f2:
        writer2 = csv.writer(f2)
        row = []
        row.extend(result["pipelines"].values())
        row.extend(result["machines"].values())
        row.append(result["total_duration"])

        writer2.writerow(row)
    # endregion


def execute_Most_Fit_Task():
    pipelines = create_pipelines()
    machines = create_VMs()

    # region Execution of Most Fit Task
    MFT = MostFitTask(machines, pipelines)
    MFT.execute_MFT()
    # endregion


if __name__ == '__main__':
    with open("./results_RR.csv", "w", newline="") as f:
        writer = csv.writer(f)
        header = ["Pipeline1", "Pipeline2", "Pipeline3", "Pipeline4",
                  "Machine1-Idle", "Machine2-Idle", "Machine3-Idle", "Total"]
        writer.writerow(header)
    for i in range(1, 5):
        execute_Round_Robin()
