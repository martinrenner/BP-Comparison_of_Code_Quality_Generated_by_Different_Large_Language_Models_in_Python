"""
Console-based Todo List Application using OOP.

This application implements a TaskManager class that manages tasks with functionalities to add, remove,
search, mark as finished, list all tasks, and clear all tasks. The implementation ensures data validation,
efficient in-memory storage, error handling, and adheres to best practices regarding modularity,
readability, and maintainability.

Each task is represented as a dictionary with the following format:
    {
        "id": int,
        "task_name": str,
        "task_description": str,
        "is_finished": bool
    }

Author: OpenAI ChatGPT
Date: 2023-10-05
"""

from typing import List, Dict


class TaskManager:
    """
    Manages tasks in an in-memory todo list.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty task collection 
        and sets the starting task ID.
        """
        self.tasks: Dict[int, Dict] = {}
        self.next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: Unique task ID for the newly added task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task given its unique ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was removed successfully, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks containing the search term in the task name or description.

        Args:
            task_term (str): The term to search for.

        Returns:
            List[Dict]: A list of tasks that match the search term.

        Raises:
            ValueError: If the search term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        results: List[Dict] = []
        task_term_lower = task_term.lower()

        for task in self.tasks.values():
            if task_term_lower in task["task_name"].lower() or task_term_lower in task["task_description"].lower():
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was successfully marked as finished, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.

        Returns:
            List[Dict]: A list of all tasks with their details.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Clears all tasks from the manager.

        Returns:
            bool: True if tasks are cleared successfully.
        """
        self.tasks.clear()
        return True


def print_task(task: Dict) -> None:
    """
    Prints a task in a formatted manner.

    Args:
        task (Dict): A task dictionary to print.
    """
    status = "Finished" if task["is_finished"] else "Pending"
    print(f'ID: {task["id"]:>3} | Name: {task["task_name"]:<20} | Description: {task["task_description"]:<30} | Status: {status}')


def main() -> None:
    """
    Main function to run the console-based todo list application.
    Presents a menu-driven interface for the user.
    """
    task_manager = TaskManager()

    menu = """
Console-based Todo List Application
--------------------------------------
1. Add a task
2. Remove a task
3. Search tasks
4. Mark a task as finished
5. Display all tasks
6. Clear all tasks
7. Exit
"""

    while True:
        print(menu)
        choice = input("Enter your choice (1-7): ").strip()

        try:
            if choice == "1":
                # Adding a task
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = task_manager.add(task_name, task_description)
                print(f"Task added with ID: {task_id}")

            elif choice == "2":
                # Removing a task
                task_id_str = input("Enter task ID to remove: ").strip()
                if not task_id_str.isdigit():
                    print("Invalid input. Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_str)
                if task_manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")

            elif choice == "3":
                # Searching for tasks
                search_term = input("Enter search term: ").strip()
                results = task_manager.search(search_term)
                if results:
                    print("Search results:")
                    for task in results:
                        print_task(task)
                else:
                    print("No matching tasks found.")

            elif choice == "4":
                # Marking a task as finished
                task_id_str = input("Enter task ID to mark as finished: ").strip()
                if not task_id_str.isdigit():
                    print("Invalid input. Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_str)
                if task_manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")

            elif choice == "5":
                # Displaying all tasks
                all_tasks = task_manager.get_all()
                if all_tasks:
                    print("All tasks:")
                    for task in all_tasks:
                        print_task(task)
                else:
                    print("No tasks found.")

            elif choice == "6":
                # Clearing all tasks
                confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirm == "yes":
                    task_manager.clear_all()
                    print("All tasks cleared.")
                else:
                    print("Operation cancelled.")

            elif choice == "7":
                print("Exiting application. Goodbye!")
                break

            else:
                print("Invalid choice. Please select a valid option.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
