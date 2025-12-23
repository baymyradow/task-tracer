from enum import Enum

class TaskStatus(str, Enum):
    TODO = "todo"
    INPROGRESS = "in-progress"
    DONE = "done"