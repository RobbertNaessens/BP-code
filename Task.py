import random


class Task:
    task_id = 1
    """
    A class to represent a single task 
    
    Attributes
    ----------
    task_id : int
        An unique way to identify the task
    task_duration : float
        The duration of the task
    priority : int
        The priority of the task
    sequential_flow : int
        The sequential flow for a task. This is important when executing the pipeline
    description : str
        Optional string to describe a task
    pipeline_id : int
        The id of the pipeline where this task belongs to
    pipeline : Pipeline
        The pipeline object where this task belongs to
    workload : float
        The simulated workload of a certain task.
    """

    def __init__(self, task_duration, priority=0, sequential_flow=0, description=""):
        """
        Constructs a Task object with a certain duration, priority, sequential_flow and description
        :param task_duration: float
        :param priority: int
        :param sequential_flow: int
        :param description: str
        """
        self.task_id = Task.task_id
        Task.task_id += 1

        self.task_duration = task_duration
        self.priority = priority
        self.sequential_flow = sequential_flow
        self.description = description

        self.pipeline_id = 0
        self.pipeline = None
        self.workload = self.simulate_workload()

    def simulate_workload(self):
        """
        This function generates a random workload for the given task based on the task duration and some random values
        :return: float
        """
        # This function will be used while executing the MFT algorithm
        return self.task_duration * round(random.uniform(2, 5), 2) * round(random.uniform(0.8, 1.2), 2)

    def set_pipeline(self, pipeline):
        """
        THis function sets a pipeline object as the parent of this task object
        :param pipeline: Pipeline
        """
        self.pipeline = pipeline
        self.pipeline_id = pipeline.pipeline_id
        self.priority = pipeline.priority

    def __str__(self):
        return f"Task {self.task_id} with priority {self.priority} has {self.task_duration} seconds remaining."
