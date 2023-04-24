from Task import *


class Pipeline:
    pipeline_id = 1

    def __init__(self, tasks_in_pipeline: list[Task], description="", priority=0):
        self.pipeline_id = Pipeline.pipeline_id
        Pipeline.pipeline_id += 1

        self.tasks = tasks_in_pipeline
        self.description = description
        self.priority = priority

        for task in self.tasks:
            task.set_pipeline(self)
