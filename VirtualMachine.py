from MachineStatus import *
import Task
import time
from threading import Lock

lock = Lock()


class VirtualMachine:
    def __init__(self, machine_id, status: MachineStatus):
        self.status = status
        self.machine_id = machine_id

    def execute_task(self, task: Task, quantum: int):
        print(f"Machine {self.machine_id}: Executing task {task.task_id}...")
        if task.task_duration < quantum:
            duration = task.task_duration
            task.task_duration = 0
            print(f"Machine {self.machine_id}: Completed task {task.task_id}")
        else:
            task.task_duration -= quantum
            duration = quantum
        time.sleep(duration)
        print(f"Machine {self.machine_id}: Done executing task {task.task_id} for {duration} seconds")
        self.change_status(MachineStatus.WAITING)
        return task

    def change_status(self, status):
        with lock:
            self.status = status
