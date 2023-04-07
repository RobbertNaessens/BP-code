from MachineStatus import *
import Task
import time
from threading import Lock

lock = Lock()


class VirtualMachine:
    vm_id = 1

    # TODO: Hardware simuleren. Zeker voor Most-fit algo is dit belangrijk

    def __init__(self, status: MachineStatus = MachineStatus.WAITING):
        self.status = status
        self.machine_id = VirtualMachine.vm_id
        VirtualMachine.vm_id += 1

        self.working_time = 0

    def execute_task(self, task: Task, quantum: int, current_time):
        print(f"Machine {self.machine_id}: Executing task {task.task_id}... (Pipeline {task.pipeline_id})")
        if task.task_duration < quantum:
            duration = task.task_duration
            task.task_duration = 0
            print(f"Machine {self.machine_id}: Completed task {task.task_id}")
        else:
            task.task_duration -= quantum
            duration = quantum
        time.sleep(duration)
        self.working_time += duration
        print(
            f"Machine {self.machine_id}: Done executing task {task.task_id} for {duration} seconds (remaning duration: {task.task_duration})")
        self.change_status(MachineStatus.WAITING)

        return task

    def change_status(self, status):
        with lock:
            self.status = status
