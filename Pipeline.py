from Task import *


class Pipeline:
    pipeline_id = 1

    def __init__(self, tasks_in_pipeline: list[Task], description=""):
        self.pipeline_id = Pipeline.pipeline_id
        Pipeline.pipeline_id += 1

        self.tasks = tasks_in_pipeline
        self.description = description

        self.assign_pipeline_id_to_tasks()

    def assign_pipeline_id_to_tasks(self):
        for task in self.tasks:
            task.pipeline_id = self.pipeline_id
