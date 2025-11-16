"""
todo.py

A tiny command-line todo manager meant for beginners.
It demonstrates:
 - reading and writing JSON files,
 - simple functions for modular code,
 - a loop-based menu for user interaction.

Usage:
    python todo.py
"""

import json
import os

# File where tasks will be stored. We choose a small JSON file.
DATA_FILE = "tasks.json"


def load_tasks():
    """
    Load tasks from DATA_FILE.
    If the file does not exist, return an empty list.

    Each task is represented as a dictionary:
      { "id": int, "title": str, "done": bool }
    """
    if not os.path.exists(DATA_FILE):
        # No file yet: start with an empty task list
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Basic validation: we expect a list
            if isinstance(data, list):
                return data
            else:
                print("Warning: data file has unexpected format, starting fresh.")
                return []
    except (json.JSONDecodeError, IOError) as e:
        # If file is corrupted or unreadable, inform and start fresh
        print("Could not read tasks file (starting empty). Error:", e)
        return []


def save_tasks(tasks):
    """
    Save the list of tasks to DATA_FILE in JSON format.
    Overwrites the file each time we save.
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print("Error saving tasks:", e)


def next_id(tasks):
    """
    Generate the next task id.
    We keep ids simple: 1 higher than current max, or 1 if empty.
    """
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1


def add_task(tasks):
    """
    Ask user for a task title and add it to tasks list.
    """
    title = input("Enter task title: ").strip()
    if not title:
        print("Empty title — task not added.")
        return

    task = {"id": next_id(tasks), "title": title, "done": False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {task['title']}")


def list_tasks(tasks):
    """
    Print tasks in a readable format.
    """
    if not tasks:
        print("No tasks yet.")
        return

    print("\nTasks:")
    for task in tasks:
        status = "✓" if task.get("done") else " "
        print(f"[{status}] {task['id']}: {task['title']}")
    print()  # blank line after list


def complete_task(tasks):
    """
    Mark a task as done by its id.
    """
    if not tasks:
        print("No tasks to complete.")
        return

    try:
        id_str = input("Enter the id of the task to mark done: ").strip()
        if not id_str:
            print("No id entered.")
            return
        task_id = int(id_str)
    except ValueError:
        print("Please enter a valid numeric id.")
        return

    for task in tasks:
        if task.get("id") == task_id:
            if task.get("done"):
                print("Task already marked done.")
            else:
                task["done"] = True
                save_tasks(tasks)
                print(f"Task #{task_id} marked done.")
            return

    print(f"No task found with id {task_id}.")


def delete_task(tasks):
    """
    Delete a task by id.
    """
    if not tasks:
        print("No tasks to delete.")
        return

    try:
        id_str = input("Enter the id of the task to delete: ").strip()
        if not id_str:
            print("No id entered.")
            return
        task_id = int(id_str)
    except ValueError:
        print("Please enter a valid numeric id.")
        return

    for i, task in enumerate(tasks):
        if task.get("id") == task_id:
            confirm = input(
                f"Delete task #{task_id} '{task['title']}'? (y/N): ").strip().lower()
            if confirm == "y":
                tasks.pop(i)
                save_tasks(tasks)
                print(f"Deleted task #{task_id}.")
            else:
                print("Delete cancelled.")
            return

    print(f"No task found with id {task_id}.")


def show_menu():
    """
    Print the menu. This keeps the UI code in one place.
    """
    print("Simple Todo CLI")
    print("----------------")
    print("1) List tasks")
    print("2) Add task")
    print("3) Mark task done")
    print("4) Delete task")
    print("5) Quit")


def main():
    """
    Main program loop:
     - load tasks
     - show menu repeatedly until user quits
    """
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
