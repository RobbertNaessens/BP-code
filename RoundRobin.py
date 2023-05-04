import concurrent.futures
import functools

from VirtualMachine import *
from Pipeline import *
from AbstractAlgorithm import *
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import time

lock = Lock()


def split_tasks_based_on_sequential_flow(pipeline_tasks):
    """
    Overrides AbstractAlgorithm.split_tasks_based_on_sequential_flow(pipeline_tasks)

    Splits all the tasks based on their sequential flow
    :param pipeline_tasks: List[Task]
    :return: List[Task]
    """
    result = []
    saved_flows = set()
    temp_list = []
    pipeline_tasks = list(sorted(pipeline_tasks, key=sort_function_for_flows))
    for task in pipeline_tasks:
        flow = task.sequential_flow
        if flow not in saved_flows:
            saved_flows.add(flow)
            result.append(temp_list)
            temp_list = [task]
        else:
            temp_list.append(task)
    result.append(temp_list)
    return result


class RoundRobin(AbstractAlgorithm):
    """
        A class that represents the Round Robin algorithm for scheduling by overwriting the abstract class AbstractAlgorithm.

        Attributes
        ----------
        tasks : List[Task]
            A sequence of tasks that needs to be executed
        pipeline_dict : dict
            A helper dictionary for gathering results per pipeline
        quantum : int
            Time quantum for executing a given task for a certain amount of time
        running_futures : List[Future]
            A list of the current running futures
        subtask_list : List[Task]
            A helper list for executing the method execute_RR

        Methods
        -------
        split_tasks_based_on_pipeline()
            Makes a new dictionary with information about each pipeline
        select_machine()
            Returns a VirtualMachine for executing a task
        execute_task_on_machine(selected_machine, current_task)
            Executes the currently selected task on the selected machine and returns the task
        execute()
            Executes the Round Robin algorithm
        return_task_to_the_pipeline_queue()
            Checks if the task was successfully executed and places it back on the queue when necessary
        get_results()
            Gathers results after execution of the algorithm
        execute_RR()
            Executes the Round Robin algorithm in a worse way
        return_task_to_the_splitted_queue()
            Checks if the task was successfully executed and places it back on the queue when necessary
        execute_RR_better()
            Executes the Round Robin algorithm in a better way
        search_next_task()
            Searches for the next available task
    """
    def __init__(self, machines: list[VirtualMachine], pipelines: list[Pipeline], quantum: int):
        super().__init__(machines, pipelines)
        self.quantum = quantum

        self.tasks = []
        self.pipeline_dict = dict()
        self.split_tasks_based_on_pipeline()

        self.running_futures = []
        self.splitted_tasks = split_tasks_based_on_sequential_flow(self.tasks)
        self.subtask_list = []

    def select_machine(self):
        """
        Returns an available VirtualMachine for executing a task
        :return: VirtualMachine
        """
        while True:
            available_machines = list(filter(lambda m: m.status == MachineStatus.WAITING, self.machines))
            if len(available_machines) > 0:
                return available_machines[0]

    def execute_task_on_machine(self, selected_machine, current_task):
        """
        Executes the currently selected task on the selected machine and returns the task
        :param selected_machine: VirtualMachine
        :param current_task: Task
        :return: Task
        """
        return selected_machine.execute_task_RR(current_task, self.quantum)

    def split_tasks_based_on_pipeline(self):
        """
        Makes a new helper dictionary with information about each pipeline

        """
        for pipeline in self.pipelines:
            splitted_tasks = split_tasks_based_on_sequential_flow(pipeline.tasks)
            self.pipeline_dict[f"{pipeline.pipeline_id}"] = {
                "tasks": splitted_tasks, "current_flow": 0,
                "amount_of_tasks": list(map(lambda t: len(t), splitted_tasks)),
                "finished": False, "total_task_counter": len(pipeline.tasks)}
            self.tasks.extend(pipeline.tasks)

    def execute_RR(self):
        """
        This function is a first version of the Round Robin algorithm. It's an improvement in comparison with the dumb algorithm, but it's still not very good

        The function loops over all the tasks while taking into account the priority of the tasks and the pipelines.
        It uses the ThreadPoolExecutor to execute tasks on machines in separate threads.
        """
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
        total_time = time.time() - self.start_time
        print(
            f"Machines Idle-time: {list(map(lambda m: total_time - m.working_time, self.machines))}; Total duration: {total_time}")

        # Free resources
        self.pool.shutdown()
        return self.get_results()

    def return_task_to_the_splitted_queue(self, future):
        """
        Checks if the task in the future is fully completed. If not, the task is sent back to the queue 
        :param future: Future
        """
        task = future.result()
        if task.task_duration > 0:
            self.subtask_list.append(task)
        else:
            pipeline = self.pipeline_dict[str(task.pipeline_id)]
            pipeline["total_task_counter"] -= 1
            if pipeline["total_task_counter"] == 0 and not pipeline["finished"]:
                pipeline["finished"] = True
                pipeline["completion_time"] = time.time() - self.start_time

    def search_next_task(self):
        """
        Searches for the next available task in the list. This function holds track of running tasks in other threads, the sequential flows of the pipelines and the priority of tasks and pipelines.
        :return: tuple
        """
        sorted_pipelines = list(sorted(self.pipelines, key=lambda p: p.priority, reverse=True))
        sorted_pipelines_ids = list(map(lambda p: p.pipeline_id, sorted_pipelines))
        pipeline_looper = 0

        # Variable to break the while loop when all pipelines are finished
        number_of_pipelines_finished = 0
        while number_of_pipelines_finished != len(self.pipeline_dict.keys()):
            number_of_pipelines_finished = len(
                list(filter(lambda p: p["finished"] is True, self.pipeline_dict.values())))
            # Hier zoeken we naar een beschikbare taak van een bepaalde pipeline
            # We houden rekening met de sequentiele flow en ook het feit dat er bepaalde tasks nog running kunnen zijn
            selected_id = sorted_pipelines_ids[pipeline_looper]

            # Gekozen pipeline
            selected_pipeline = self.pipeline_dict[str(selected_id)]

            # Check of er nog remaining tasks zijn
            # (deze kunnen momenteel ook nog uitgevoerd worden door een andere thread)
            if len(selected_pipeline["amount_of_tasks"]) > 0 and not selected_pipeline["finished"]:
                remaining_tasks = selected_pipeline["amount_of_tasks"][0]
                if remaining_tasks < 1:
                    # Voor de current flow zijn er geen taken meer
                    # current flow increasen en lege array poppen
                    selected_pipeline["current_flow"] += 1
                    selected_pipeline["tasks"].pop(0)
                    selected_pipeline["amount_of_tasks"].pop(0)

                # In het ander geval kan het zijn dat er taken nog runnende zijn en dus niet terug in de queue staan
                # in dit geval is de lengte vd array = 0
                elif len(selected_pipeline["tasks"]) > 0 and len(selected_pipeline["tasks"][0]) == 0:
                    # Switch naar een andere pipeline
                    pipeline_looper = (pipeline_looper + 1) % len(sorted_pipelines_ids)

                # In het ander geval is een taak beschikbaar
                else:
                    return selected_pipeline["tasks"][0].pop(0), selected_id
            else:
                # Geen taken meer op deze pipeline
                # Zoeken op de volgende pipeline
                if not selected_pipeline["finished"]:
                    selected_pipeline["finished"] = True
                    selected_pipeline["completion_time"] = time.time() - self.start_time
                pipeline_looper = (pipeline_looper + 1) % len(sorted_pipelines_ids)
        return None, 0

    def execute_RR_better(self):
        """
        Executes the Round Robin algorithm by searching for a next task and executing this task on a certain machine in a separate thread
        :return: dict
        """
        selected_task, pipeline_id = self.search_next_task()
        while selected_task is not None:
            selected_machine = self.select_machine()
            selected_machine.change_status(MachineStatus.RUNNING)
            future = self.pool.submit(self.execute_task_on_machine, selected_machine, selected_task)
            future.add_done_callback(
                functools.partial(self.return_task_to_the_pipeline_queue, pipeline_id))
            with lock:
                selected_task, pipeline_id = self.search_next_task()

        # Free resources
        self.pool.shutdown()
        return self.get_results()

    def execute(self):
        """
        Executes the function execute_RR_better
        :return: dict
        """
        return self.execute_RR_better()

    def return_task_to_the_pipeline_queue(self, pipeline_id, future):
        """
        Checks if the task in the future is fully completed. If not, the task is sent back to the queue of the right pipeline
        :param pipeline_id: int
        :param future: Future
        """
        task = future.result()
        if task.task_duration > 0:
            # Append the task to the right pipeline
            self.pipeline_dict[str(pipeline_id)]["tasks"][0].append(task)
        else:
            self.pipeline_dict[str(pipeline_id)]["amount_of_tasks"][0] -= 1

    def get_results(self):
        """
        Collects the results after execution from the pipeline_dict and returns them
        :return: dict
        """
        print("\n############################################################\n")
        total_time = time.time() - self.start_time
        result_dict = dict({"pipelines": dict(), "machines": dict(), "total_duration": total_time})
        for pipeline_id in self.pipeline_dict.keys():
            print(f"Pipeline {pipeline_id} completed in {self.pipeline_dict[pipeline_id]['completion_time']} seconds")
            result_dict["pipelines"][pipeline_id] = self.pipeline_dict[pipeline_id]['completion_time']
        for machine in self.machines:
            print(f"Machine {machine.machine_id} idle time: {total_time - machine.working_time} seconds")
            result_dict["machines"][machine.machine_id] = total_time - machine.working_time
        print(f"Total duration: {total_time} seconds")
        return result_dict
