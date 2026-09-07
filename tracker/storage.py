import json
from pathlib import Path

from .models import Task

def load_tasks(path: Path) -> list[Task]:
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Task.from_dict(d) for d in raw]

def save_tasks(tasks: list[Task], path: Path) -> None:
    data = [t.to_dict() for t in tasks]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f,ensure_ascii=False, indent=2)
