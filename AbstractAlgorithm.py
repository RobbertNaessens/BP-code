from abc import ABC, abstractmethod
from VirtualMachine import *
from Pipeline import *
from concurrent.futures import ThreadPoolExecutor


def sort_function_for_flows(task: Task):
    return task.sequential_flow


def sort_function(task: Task):
    return task.priority


@abstractmethod
def split_tasks_based_on_sequential_flow(pipeline_tasks):
    pass


class AbstractAlgorithm(ABC):
    def __init__(self, machines: list[VirtualMachine], pipelines: list[Pipeline]):
        self.machines = machines
        self.pipelines = pipelines
        self.pool = ThreadPoolExecutor(max_workers=len(machines))
        self.start_time = time.time()

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_results(self):
        pass

    @abstractmethod
    def select_machine(self):
        pass

    @abstractmethod
    def execute_task_on_machine(self, machine, task):
        pass
