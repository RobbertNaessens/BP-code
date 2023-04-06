import concurrent.futures

from VirtualMachine import *
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

lock = Lock()


def sort_function(task: Task):
    return task.priority


class RoundRobin:
    def __init__(self, machines: list[VirtualMachine], tasks: list[Task], quantum: int):
        self.tasks = tasks
        self.quantum = quantum
        self.machines = machines
        self.pool = ThreadPoolExecutor(max_workers=len(machines))

        self.running_futures = []
        self.splitted_tasks = self.split_tasks_based_on_sequential_flow()
        self.subtask_list = []

    def split_tasks_based_on_sequential_flow(self):
        result = []
        saved_flows = set()
        temp_list = []
        for task in self.tasks:
            flow = task.sequential_flow
            if flow not in saved_flows:
                saved_flows.add(flow)
                result.append(temp_list)
                temp_list = [task]
            else:
                temp_list.append(task)
        result.append(temp_list)
        return result

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
            while len(self.tasks) > 0:
                self.tasks = deque(sorted(self.tasks, key=sort_function, reverse=True))
                current_task = self.tasks.popleft()
                selected_machine = self.select_machine()
                selected_machine.change_status(MachineStatus.RUNNING)
                future = self.pool.submit(self.execute_task_on_machine, selected_machine, current_task)
                future.add_done_callback(self.return_task_to_the_queue)
                self.running_futures.append(future)
            concurrent.futures.wait(self.running_futures)
            self.running_futures = []
        # print("Round Robin executed")

    def execute2(self):
        while len(self.splitted_tasks) > 0:
            self.subtask_list = self.splitted_tasks[0]
            while len(self.subtask_list) > 0:
                while len(self.subtask_list) > 0:
                    self.subtask_list = deque(sorted(self.subtask_list, key=sort_function, reverse=True))
                    current_task = self.subtask_list.popleft()
                    selected_machine = self.select_machine()
                    selected_machine.change_status(MachineStatus.RUNNING)
                    future = self.pool.submit(self.execute_task_on_machine, selected_machine, current_task)
                    future.add_done_callback(self.return_task_to_the_splitted_queue)
                    self.running_futures.append(future)
                concurrent.futures.wait(self.running_futures)
                self.running_futures = []
            self.splitted_tasks.pop(0)


    def return_task_to_the_splitted_queue(self, future):
        task = future.result()
        if task.task_duration > 0:
            self.subtask_list.append(task)
