from RoundRobin import *
from VirtualMachine import *
from Task import *

if __name__ == '__main__':
    task1 = Task(180, sequential_flow=1, description="Process finance data")
    task2 = Task(20.9, sequential_flow=1, description="Process finance data")

    task3 = Task(15.8, sequential_flow=2, description="P&L x Transaction Lines")
    task4 = Task(22.1, sequential_flow=2, description="B/S x Transaction Lines")
    task5 = Task(4.7, sequential_flow=2, description="GL Account")
    task6 = Task(8.3, sequential_flow=2, description="Budget Cost Center")

    task7 = Task(0.8, sequential_flow=3, description="postings")
    task8 = Task(3.2, sequential_flow=3, description="transaction_lines")
    task9 = Task(0.1, sequential_flow=3, description="accounts")




    tasks = [task1, task2, task3, task4, task5]

    time_quantum = 3

    m1 = VirtualMachine(1, MachineStatus.WAITING)
    m2 = VirtualMachine(2, MachineStatus.WAITING)
    machines = [m1, m2]

    RR = RoundRobin(machines, deque(tasks), time_quantum)
    RR.execute()

