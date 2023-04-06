from RoundRobin import *
from VirtualMachine import *
from Task import *
from Pipeline import *

if __name__ == '__main__':
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
    p2_task1 = Task(0.1, sequential_flow=1, description="Clear cache")

    p2_task2 = Task(33.5, sequential_flow=2, description="Run data set compressions")

    p2_task3 = Task(1.0, sequential_flow=3, description="Fill data set models cache")
    # endregion

    p1_tasks = [p1_task1, p1_task2, p1_task3, p1_task4, p1_task5, p1_task6, p1_task7, p1_task8, p1_task9,
                p1_task10, p1_task11, p1_task12, p1_task13, p1_task14, p1_task15, p1_task16, p1_task17, p1_task18,
                p1_task19, p1_task20, p1_task21]
    pipeline1 = Pipeline(p1_tasks, "Process finance data")

    p2_tasks = [p2_task1, p2_task2, p2_task3]
    pipeline2 = Pipeline(p2_tasks, "Run data set compression")

    time_quantum = 5

    m1 = VirtualMachine()
    m2 = VirtualMachine()
    m3 = VirtualMachine()
    machines = [m1, m2, m3]

    RR = RoundRobin(machines, pipeline1.tasks, time_quantum)
    RR.execute2()
