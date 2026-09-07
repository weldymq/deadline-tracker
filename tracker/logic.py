from datetime import date
from .models import Task

def days_left(task: Task, today: date | None = None) -> int:
    if today == None:
        today = date.today()
    deadline = task.deadline
    days_left = (deadline - today).days
    return days_left

def is_overdue(task: Task, today: date | None = None) -> bool:
    if task.done:
        return False
    return days_left(task, today) < 0

def sort_by_urgency(tasks: list[Task]) -> list[Task]:
    return sorted(tasks, key=lambda t: t.deadline)