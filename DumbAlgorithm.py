from collections import deque
import concurrent.futures
import functools

from VirtualMachine import *
from Pipeline import *
from concurrent.futures import ThreadPoolExecutor
import time


def sort_function_for_flows(task: Task):
    return task.sequential_flow


def sort_function(task: Task):
    return task.priority


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


class DumbAlgorithm:
    def __init__(self, machines: list[VirtualMachine], pipelines: list[Pipeline]):
        self.pipelines = pipelines
        self.machines = machines

        self.pool = ThreadPoolExecutor(max_workers=len(machines))
        self.tasks = []
        self.pipeline_dict = dict()
        self.split_tasks_based_on_pipeline()

        self.running_futures = []
        self.splitted_tasks = split_tasks_based_on_sequential_flow(self.tasks)
        self.subtask_list = []

        self.start_time = time.time()

    def split_tasks_based_on_pipeline(self):
        for pipeline in list(sorted(self.pipelines, key=lambda p: p.priority, reverse=True)):
            splitted_tasks = split_tasks_based_on_sequential_flow(pipeline.tasks)
            self.pipeline_dict[f"{pipeline.pipeline_id}"] = {
                "tasks": splitted_tasks, "current_flow": 0,
                "amount_of_tasks": list(map(lambda t: len(t), splitted_tasks)),
                "finished": False, "total_task_counter": len(pipeline.tasks)}
            self.tasks.extend(pipeline.tasks)

    def select_machine(self):
        while True:
            available_machines = list(filter(lambda m: m.status == MachineStatus.WAITING, self.machines))
            if len(available_machines) > 0:
                return available_machines[0]

    def execute_task_on_machine(self, selected_machine, current_task):
        return selected_machine.execute_task_Dumb(current_task)

    def execute(self):
        for pipeline_id in self.pipeline_dict.keys():
            selected_pipeline = self.pipeline_dict[str(pipeline_id)]
            while len(selected_pipeline["amount_of_tasks"]) > 0 and not selected_pipeline["finished"]:
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
                    # Hier even wachten en later opnieuw proberen
                    time.sleep(0.1)
                # In het ander geval is een taak beschikbaar
                else:
                    available_task = selected_pipeline["tasks"][0].pop(0)
                    selected_machine = self.select_machine()
                    selected_machine.change_status(MachineStatus.RUNNING)
                    future = self.pool.submit(self.execute_task_on_machine, selected_machine, available_task)
                    future.add_done_callback(
                        functools.partial(self.return_task_to_the_pipeline_queue, pipeline_id))
            if not selected_pipeline["finished"]:
                selected_pipeline["finished"] = True
                selected_pipeline["completion_time"] = time.time() - self.start_time

        total_time = time.time() - self.start_time
        print(
            f"Machines Idle-time: {list(map(lambda m: total_time - m.working_time, self.machines))}; Total duration: {total_time}")

        # Free resources
        self.pool.shutdown()
        return self.get_results()

    def return_task_to_the_pipeline_queue(self, pipeline_id, future):
        print("CALLBACK")
        task = future.result()
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
