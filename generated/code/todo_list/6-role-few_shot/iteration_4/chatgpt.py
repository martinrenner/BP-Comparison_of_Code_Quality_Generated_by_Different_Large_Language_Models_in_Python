import sys


class TaskManager:
    """
    Manages tasks in an in-memory store with functionalities to add, remove,
    search, finish, retrieve, and clear tasks.

    Each task is stored as a dictionary in the following format:
        {
            'id': int,
            'task_name': str,
            'task_description': str,
            'is_finished': bool
        }
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task store and sets the next unique task ID.
        """
        self._tasks = {}  # Dictionary to store tasks with task_id as key
        self._next_id = 1  # Incremental id used when adding new tasks

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task store.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the task.

        Raises:
            ValueError: If either task_name or task_description is an empty string.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name,
            'task_description': task_description,
            'is_finished': False
        }
        self._next_id += 1

        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes the task with the specified task_id.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if the task was removed, False if task_id does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Searches for tasks that contain the search term in the task name or description.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of tasks that match the search criteria.

        Raises:
            ValueError: If task_term is an empty string.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        task_term_lower = task_term.lower()

        matching_tasks = [
            task for task in self._tasks.values()
            if task_term_lower in task['task_name'].lower() or task_term_lower in task['task_description'].lower()
        ]
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks the specified task as finished.

        Args:
            task_id (int): The unique ID of the task to mark as finished.

        Returns:
            bool: True if the task was successfully marked as finished,
                  False if the task does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            self._tasks[task_id]['is_finished'] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all tasks from the task store.

        Returns:
            list[dict]: A list of all tasks with their details.
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Removes all tasks from the task store.

        Returns:
            bool: True if all tasks were cleared.
        """
        self._tasks.clear()
        return True


def display_menu() -> None:
    """
    Displays the menu options for the console-based to-do list application.
    """
    menu = (
        "\nTo-Do List Application\n"
        "-----------------------\n"
        "1. Add Task\n"
        "2. Remove Task\n"
        "3. Search Tasks\n"
        "4. Finish Task\n"
        "5. Get All Tasks\n"
        "6. Clear All Tasks\n"
        "7. Exit\n"
        "Enter your choice (1-7): "
    )
    print(menu, end='')


def run_console():
    """
    Runs the console-based interface for the to-do list application.
    """
    manager = TaskManager()

    while True:
        try:
            display_menu()
            choice = input().strip()

            if choice == '1':
                # Add Task
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = manager.add(task_name, task_description)
                print(f"Task added with ID: {task_id}")

            elif choice == '2':
                # Remove Task
                try:
                    task_id = int(input("Enter task ID to remove: ").strip())
                except ValueError:
                    print("Invalid input. Please enter a valid positive integer for task ID.")
                    continue

                if manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"No task found with ID {task_id}.")

            elif choice == '3':
                # Search Tasks
                task_term = input("Enter search term: ").strip()
                results = manager.search(task_term)
                if results:
                    print("Matching tasks:")
                    for task in results:
                        print(task)
                else:
                    print("No matching tasks found.")

            elif choice == '4':
                # Finish Task
                try:
                    task_id = int(input("Enter task ID to mark as finished: ").strip())
                except ValueError:
                    print("Invalid input. Please enter a valid positive integer for task ID.")
                    continue

                if manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
                else:
                    print(f"No task found with ID {task_id}.")

            elif choice == '5':
                # Get All Tasks
                tasks = manager.get_all()
                if tasks:
                    print("All tasks:")
                    for task in tasks:
                        print(task)
                else:
                    print("No tasks available.")

            elif choice == '6':
                # Clear All Tasks
                confirmation = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirmation == 'yes':
                    manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear all tasks aborted.")

            elif choice == '7':
                # Exit
                print("Exiting application.")
                sys.exit(0)

            else:
                print("Invalid choice. Please select a valid option.")

        except ValueError as ve:
            # Handle known validation errors
            print(f"Error: {ve}")
        except Exception as e:
            # Generic error handler
            print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    run_console()
