from abc import ABC, abstractmethod
from VirtualMachine import *
from Pipeline import *
from concurrent.futures import ThreadPoolExecutor


def sort_function_for_flows(task: Task):
    """
    Sort function for tasks based on sequential flow
    :param task: Task
    :return: int
    """
    return task.sequential_flow


def sort_function(task: Task):
    """
    Sort function for tasks based on priority
    :param task: Task
    :return: int
    """
    return task.priority


@abstractmethod
def split_tasks_based_on_sequential_flow(pipeline_tasks):
    """
    Splits all the tasks based on their sequential flow
    :param pipeline_tasks: List[Task]
    :return: List[Task]
    """
    pass


class AbstractAlgorithm(ABC):
    """
    A class to represent an abstract level of the different algorithms

    Attributes
    ----------
    machines : list[VirtualMachine]
        the machines that will be used in the algorithm (class VirtualMachine)
    pipelines : list[Pipeline]
        the pipelines that will be processed in the algorithm (class Pipeline)
    pool : ThreadPoolExecutor
        a pool of threads to simulate parallel work
    start_time : time
        the start time of the algorithm when it generated

    Methods
    -------
    execute()
        executes the algorithm
    get_results()
        gathers and returns the results after executing the algorithm
    select_machine()
        algorithm-specific function to select the next machine
    execute_task_on_machine(selected_machine, current_task)
        algorithm-specific way of running a task on a virtual machine
    """
    def __init__(self, machines: list[VirtualMachine], pipelines: list[Pipeline]):
        """

        Parameters
        ----------
        machines : list[VirtualMachine]
            the machines that will be used in the algorithm (class VirtualMachine)
        pipelines : list[Pipeline]
            the pipelines that will be processed in the algorithm (class Pipeline)
        """
        self.machines = machines
        self.pipelines = pipelines
        self.pool = ThreadPoolExecutor(max_workers=len(machines))
        self.start_time = time.time()

    @abstractmethod
    def execute(self):
        """
        Defines a way to execute the algorithm
        :return: dict
        """
        pass

    @abstractmethod
    def get_results(self):
        """
        Gathers the results after executing the algorithm
        :return: dict
        """
        pass

    @abstractmethod
    def select_machine(self):
        """
        Selects the next machine for execution
        :return: VirtualMachine
        """
        pass

    @abstractmethod
    def execute_task_on_machine(self, machine, task):
        """
        Executes the task on a virtual machine
        :param machine: VirtualMachine
        :param task: Task
        :return: Task
        """
        pass
