from dataclasses import dataclass
from datetime import date

@dataclass
class Task:
    id: int
    title: str
    deadline: date
    done: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "deadline": self.deadline.isoformat(),
            "done": self.done
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            deadline=date.fromisoformat(data["deadline"]),
            done=data["done"]
        )


if __name__ == "__main__":
    t = Task(1, "sdat labu", date(2026,9,15))
    d = t.to_dict()
    print(d)
    print(Task.from_dict(d))
    print(Task.from_dict(d) == t)