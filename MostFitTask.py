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


def calculate_fitness(machine: VirtualMachine, task: Task):
    # We calculate the fitness of a given task and machine
    # To do this, we use the formula provided in the paper
    expected_execution_time = task.workload / machine.clock_speed
    diff = abs(expected_execution_time - task.task_duration)
    fitness = 10000 / (1 + diff)
    return fitness


def split_tasks_based_on_sequential_flow(pipeline_tasks):
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


def sort_function_for_flows(task: Task):
    return task.sequential_flow


class MostFitTask(AbstractAlgorithm):
    def __init__(self, machines: list[VirtualMachine], pipelines: list[Pipeline]):
        super().__init__(machines, pipelines)
        self.tasks = []
        self.pipeline_dict = dict()
        self.split_tasks_based_on_pipeline()
        self.selected_task = None

    def select_machine(self):
        task = self.selected_task
        while True:
            available_machines = list(filter(lambda m: m.status == MachineStatus.WAITING, self.machines))
            if len(available_machines) > 0:
                fitness_values = list(calculate_fitness(machine, task) for machine in available_machines)
                selected_machine_id = fitness_values.index(max(fitness_values))
                return available_machines[selected_machine_id]

    def execute_task_on_machine(self, selected_machine: VirtualMachine, current_task):
        return selected_machine.execute_task_MFTF(current_task)

    def split_tasks_based_on_pipeline(self):
        for pipeline in self.pipelines:
            splitted_tasks = split_tasks_based_on_sequential_flow(pipeline.tasks)
            self.pipeline_dict[f"{pipeline.pipeline_id}"] = {
                "tasks": splitted_tasks, "current_flow": 0,
                "amount_of_tasks": list(map(lambda t: len(t), splitted_tasks)),
                "finished": False}
            self.tasks.extend(pipeline.tasks)

    def search_next_task(self):
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

    def execute(self):
        selected_task, pipeline_id = self.search_next_task()
        while selected_task is not None:
            self.selected_task = selected_task
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

    def return_task_to_the_pipeline_queue(self, pipeline_id, future):
        task = future.result()
        # In MFT, the tasks will always be executed fully, so this is
        # just a safety measure
        if task.task_duration > 0:
            # Append the task to the right pipeline
            self.pipeline_dict[str(pipeline_id)]["tasks"][0].append(task)
        else:
            self.pipeline_dict[str(pipeline_id)]["amount_of_tasks"][0] -= 1

    def get_results(self):
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
