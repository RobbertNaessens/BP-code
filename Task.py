class Task:
    task_id = 1

    def __init__(self, task_duration, priority=0, sequential_flow=0, description=""):
        self.task_id = Task.task_id
        Task.task_id += 1

        self.task_duration = task_duration
        self.parent_task_id = 0
        self.priority = priority
        self.sequential_flow = sequential_flow
        self.subtasks = []

    def __str__(self):
        return f"Task {self.task_id} with priority {self.priority} has {self.task_duration} seconds remaining."

    def set_parent_task_id(self, task_id):
        self.parent_task_id = task_id

    def assign_subtask(self, subtask):
        subtask.set_parent_task_id(self.task_id)
        self.subtasks.append(subtask)
