import random


class Task:
    task_id = 1

    def __init__(self, task_duration, priority=0, sequential_flow=0, description=""):
        self.task_id = Task.task_id
        Task.task_id += 1

        self.task_duration = task_duration
        self.priority = priority
        self.sequential_flow = sequential_flow
        self.description = description

        self.pipeline_id = 0
        self.workload = self.simulate_workload()

    def simulate_workload(self):
        # This function will be used while executing the MFT algorithm
        return self.task_duration * round(random.uniform(2, 5), 2) * round(random.uniform(0.8, 1.2), 2)

    def __str__(self):
        return f"Task {self.task_id} with priority {self.priority} has {self.task_duration} seconds remaining."
