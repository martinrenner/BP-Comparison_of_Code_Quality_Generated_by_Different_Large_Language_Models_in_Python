import sys


class TaskManager:
    """
    A TaskManager class to manage a todo list with functionality to add, remove,
    search, finish, retrieve all tasks, and clear all tasks.
    
    Each task is stored in the following format:
        {
            "id": int,
            "task_name": str,
            "task_description": str,
            "is_finished": bool
        }
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty in-memory storage for tasks and a counter
        for generating unique task IDs.
        """
        self._tasks = {}
        self._next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the todo list.

        Args:
            task_name (str): The name of the task. Must be a non-empty string.
            task_description (str): The description of the task. Must be a non-empty string.

        Returns:
            int: The unique ID of the added task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self._next_id
        task = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self._tasks[task_id] = task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the todo list based on its ID.

        Args:
            task_id (int): The unique ID of the task to be removed. Must be a positive integer.

        Returns:
            bool: True if the task was successfully removed, False if the task ID does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        else:
            return False

    def search(self, task_term: str) -> list:
        """
        Searches for tasks whose name or description contains the given search term (case-insensitive).

        Args:
            task_term (str): The keyword(s) to search for in task names and descriptions.

        Returns:
            list[dict]: A list of tasks matching the search term.
        
        Raises:
            ValueError: If task_term is an empty string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        result = []
        term = task_term.strip().lower()
        for task in self._tasks.values():
            if term in task["task_name"].lower() or term in task["task_description"].lower():
                result.append(task)
        return result

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished based on its unique ID.

        Args:
            task_id (int): The unique ID of the task to mark as finished.

        Returns:
            bool: True if the task was successfully marked finished, False if the task ID does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            self._tasks[task_id]["is_finished"] = True
            return True
        else:
            return False

    def get_all(self) -> list:
        """
        Retrieves all tasks in the todo list.

        Returns:
            list[dict]: A list containing all tasks with their details.
        """
        # Returning a sorted list by task id for consistency.
        return [self._tasks[tid] for tid in sorted(self._tasks.keys())]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the todo list.

        Returns:
            bool: True upon successful deletion of all tasks.
        """
        self._tasks.clear()
        # Optionally reset the task ID counter.
        self._next_id = 1
        return True


def print_task(task: dict) -> None:
    """
    Prints the task details in the format: (id, task_name, task_description, is_finished)
    
    Args:
        task (dict): The task dictionary.
    """
    print(f"({task['id']}, {task['task_name']}, {task['task_description']}, {task['is_finished']})")


def main():
    """
    Entry point for the console-based todo list application.
    Provides a simple command menu and handles user interaction.
    """
    manager = TaskManager()

    menu = """
    === Todo List Menu ===
    1. add       - Add a new task
    2. remove    - Remove a task by its ID
    3. search    - Search tasks by term
    4. finish    - Mark a task as finished
    5. get_all   - Display all tasks
    6. clear_all - Delete all tasks
    7. exit      - Exit the application
    """

    while True:
        print(menu)
        choice = input("Enter a command (add, remove, search, finish, get_all, clear_all, exit): ").strip().lower()

        try:
            if choice == "add" or choice == "1":
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = manager.add(task_name, task_description)
                print(f"Task added with ID: {task_id}")

            elif choice == "remove" or choice == "2":
                try:
                    task_id = int(input("Enter task ID to remove: ").strip())
                    if manager.remove(task_id):
                        print(f"Task with ID {task_id} removed successfully.")
                    else:
                        print(f"No task found with ID {task_id}.")
                except ValueError as ve:
                    print("Invalid input. Task ID must be a positive integer.")

            elif choice == "search" or choice == "3":
                search_term = input("Enter search term: ").strip()
                results = manager.search(search_term)
                if results:
                    print("Search results:")
                    for task in results:
                        print_task(task)
                else:
                    print("No matching tasks found.")

            elif choice == "finish" or choice == "4":
                try:
                    task_id = int(input("Enter task ID to mark as finished: ").strip())
                    if manager.finish(task_id):
                        print(f"Task with ID {task_id} marked as finished.")
                    else:
                        print(f"No task found with ID {task_id}.")
                except ValueError as ve:
                    print("Invalid input. Task ID must be a positive integer.")

            elif choice == "get_all" or choice == "5":
                tasks = manager.get_all()
                if tasks:
                    print("All tasks:")
                    for task in tasks:
                        print_task(task)
                else:
                    print("No tasks available.")

            elif choice == "clear_all" or choice == "6":
                confirm = input("Are you sure you want to delete all tasks? (yes/no): ").strip().lower()
                if confirm == "yes":
                    manager.clear_all()
                    print("All tasks have been deleted.")
                else:
                    print("Clear all tasks cancelled.")

            elif choice == "exit" or choice == "7":
                print("Exiting the application. Goodbye!")
                sys.exit(0)

            else:
                print("Invalid command. Please try again.")

        except ValueError as e:
            # Gracefully handle any validation errors
            print(f"Error: {e}")
        except Exception as e:
            # Generic error handling for unforeseen exceptions
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
