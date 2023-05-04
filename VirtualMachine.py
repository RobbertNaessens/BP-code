from MachineStatus import *
import Task
import time
from threading import Lock

lock = Lock()


class VirtualMachine:
    vm_id = 1
    """
        A class to represent a single task 

        Attributes
        ----------
        status : MachineStatus
            Gives the current status of the machine
        clock_speed : float
            Simulates the clock_speed of a virtual machine to differentiate the machines and this will be used in the MFT algorithm
        machine_id : int
            An unique way to identify the virtual machine
        working_time : int
            The total amount of time this machine was working or processing tasks
        """

    def __init__(self, status: MachineStatus = MachineStatus.WAITING, clock_speed=2.6):
        """
        Constructs a VirtualMachine object with the waiting-status and e certain clock speed for the simulated CPU
        :param status: MachineStatus
        :param clock_speed: float
        """
        self.status = status
        self.clock_speed = clock_speed
        self.machine_id = VirtualMachine.vm_id
        VirtualMachine.vm_id += 1

        self.working_time = 0

    def execute_task_RR(self, task: Task, quantum: int):
        """
        Executes a selected task on this machine for a certain quantum time and returns the task afterwards
        :param task: Task
        :param quantum: int
        :return: Task
        """
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
        """
        Executes a selected task on this machine and returns the task afterwards
        :param task: Task
        :return: Task
        """
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
        """
        Executes a selected task on this machine and returns the task afterwards
        :param task: Task
        :return: Task
        """
        result_task = self.execute_task_MFTF(task)
        return result_task

    def change_status(self, status):
        """
        Changes the status of the machine in a thread-safe way
        :param status: MachineStatus
        """
        with lock:
            self.status = status
