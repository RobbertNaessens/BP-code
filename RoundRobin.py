from VirtualMachine import *
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

lock = Lock()


def sort_function(task: Task):
    return task.priority


class RoundRobin:
    def __init__(self, machines: list[VirtualMachine], tasks: deque[Task], quantum: int):
        self.tasks = tasks
        self.quantum = quantum
        self.machines = machines
        self.pool = ThreadPoolExecutor(max_workers=len(machines))

    def select_machine(self):
        while True:
            available_machines = list(filter(lambda m: m.status == MachineStatus.WAITING, self.machines))
            if len(available_machines) > 0:
                return available_machines[0]

    def execute_task_on_machine(self, selected_machine, current_task):
        return selected_machine.execute_task(current_task, self.quantum)

    def return_task_to_the_queue(self, future):
        task = future.result()
        if task.task_duration > 0:
            self.tasks.append(task)

    def execute(self):
        while len(self.tasks) > 0:
            self.tasks = deque(sorted(self.tasks, key=sort_function, reverse=True))
            current_task = self.tasks.popleft()
            selected_machine = self.select_machine()
            selected_machine.change_status(MachineStatus.RUNNING)
            future = self.pool.submit(self.execute_task_on_machine, selected_machine, current_task)
            future.add_done_callback(self.return_task_to_the_queue)
        # print("Round Robin executed")
