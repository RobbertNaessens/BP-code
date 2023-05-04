from Task import *


class Pipeline:
    """
    A class to represent a certain pipelines

    Attributes
    ----------
    pipeline_id : int
        An unique id to identify the pipeline
    tasks : List[Task]
        The list of tasks of the pipeline
    description : str
        Description of a pipeline (default is "")
    priority : the priority of the pipeline (default 0)
    """
    pipeline_id = 1

    def __init__(self, tasks_in_pipeline: list[Task], description="", priority=0):
        """
        Constructs a Pipeline object with a number of tasks, a description and a priority
        :param tasks_in_pipeline: List[Task]
        :param description: str (default is "")
        :param priority: int (default is 0)
        """
        self.pipeline_id = Pipeline.pipeline_id
        Pipeline.pipeline_id += 1

        self.tasks = tasks_in_pipeline
        self.description = description
        self.priority = priority

        for task in self.tasks:
            task.set_pipeline(self)
