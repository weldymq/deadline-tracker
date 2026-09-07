import argparse
from pathlib import Path 
from datetime import date

from .logic import days_left, is_overdue, sort_by_urgency
from .models import Task
from .storage import load_tasks, save_tasks

DATA_FILE = Path("tasks.json")


def cmd_list() -> None:
    tasks = load_tasks(DATA_FILE)
    if not tasks:
        print("Задач нет")
        return 
    for task in sort_by_urgency(tasks):
        if task.done:
            status = "Выполнено"
        elif is_overdue(task):
            status = "Просрочено"
        else:
            left = days_left(task)
            if left == 0:
                status = "Сегодня"
            else:
                status = f"Осталось {left} дн."
        print(f"[{task.id}] {task.title} - {task.deadline} ({status})")

def cmd_add(title: str, deadline_str: str) -> None:
    tasks = load_tasks(DATA_FILE)
    deadline = date.fromisoformat(deadline_str)
    new_id = max((t.id for t in tasks), default=0) + 1

    task = Task(id=new_id, title=title, deadline=deadline)
    tasks.append(task)
    save_tasks(tasks, DATA_FILE)

    print(f"Добавлено: [{new_id}] {title} — {deadline}")

def cmd_done(task_id: int) -> None:
    tasks = load_tasks(DATA_FILE)

    for task in tasks:
        if task.id == task_id:
            task.done = True
            save_tasks(tasks, DATA_FILE)
            print(f"Выполнено: [{task.id}] {task.title}")
            return 
    print(f"Задача с id {task_id} не найдена.")

def cmd_remove(task_id: int) -> None:
    tasks = load_tasks(DATA_FILE)

    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            save_tasks(tasks,DATA_FILE)
            print(f"Удалено: [{task.id}] {task.title}")
            return 
    print(f"Задача с id {task_id} не найдена.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Трекер дедлайнов")
    sub = parser.add_subparsers(dest="command", required=True)
    p_add = sub.add_parser("add", help="добавить задачу")
    p_add.add_argument("title")
    p_add.add_argument("deadline")

    p_list = sub.add_parser("list", help="показать задачи")
    p_done = sub.add_parser("done", help="отметить выполненной")
    p_done.add_argument("id", type=int)
    p_remove = sub.add_parser("remove", help="удалить задачу")
    p_remove.add_argument("id", type=int)

    args = parser.parse_args()

    if args.command == "list":
        cmd_list()
    elif args.command == "add":
        cmd_add(args.title, args.deadline)
    elif args.command == "done":
        cmd_done(args.id)
    elif args.command == "remove":
        cmd_remove(args.id)


if __name__ == "__main__":
    main()