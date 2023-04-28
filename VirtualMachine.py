from MachineStatus import *
import Task
import time
from threading import Lock

lock = Lock()


class VirtualMachine:
    vm_id = 1

    def __init__(self, status: MachineStatus = MachineStatus.WAITING, clock_speed=2.6):
        self.status = status
        self.clock_speed = clock_speed
        self.machine_id = VirtualMachine.vm_id
        VirtualMachine.vm_id += 1

        self.working_time = 0

    def execute_task_RR(self, task: Task, quantum: int):
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
            f"Machine {self.machine_id}: Done executing task {task.task_id} for {duration} seconds (remaning duration: {task.task_duration} seconds)")
        self.change_status(MachineStatus.WAITING)

        return task

    def execute_task_MFTF(self, task: Task):
        print(f"Machine {self.machine_id}: Executing task {task.task_id}... (Pipeline {task.pipeline_id}, flow {task.sequential_flow})")
        duration = task.task_duration
        task.task_duration = 0
        time.sleep(duration)
        self.working_time += duration
        print(f"Machine {self.machine_id}: Completed task {task.task_id}")
        print(
            f"Machine {self.machine_id}: Done executing task {task.task_id} for {duration} seconds (remaning duration: {task.task_duration} seconds)")
        self.change_status(MachineStatus.WAITING)

        return task

    def execute_task_Dumb(self, task):
        result_task = self.execute_task_MFTF(task)
        return result_task

    def change_status(self, status):
        with lock:
            self.status = status
