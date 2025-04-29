class TaskManager:
    """
    A class to manage tasks in a to-do list application.
    
    Each task is represented as a dictionary with the following keys:
        id (int): Unique task identifier.
        task_name (str): The name/title of the task.
        task_description (str): A detailed description of the task.
        is_finished (bool): Status flag indicating if the task is completed.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task storage and a counter for task IDs.
        """
        self._tasks = {}  # Stores tasks by their unique ID for O(1) access.
        self._next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager and returns its unique ID.

        Args:
            task_name (str): The name of the task. Must not be empty.
            task_description (str): The description of the task. Must not be empty.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed.

        Raises:
            ValueError: If task_id is negative or not an integer.
            KeyError: If a task with the given ID does not exist.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist.")

        del self._tasks[task_id]
        return True

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks whose name or description contains the provided term.

        Args:
            task_term (str): The search term. Must not be empty.

        Returns:
            list[dict]: A list of task dictionaries matching the search criteria.
                        Each dictionary is in the format:
                        {
                            'id': int,
                            'task_name': str,
                            'task_description': str,
                            'is_finished': bool
                        }

        Raises:
            ValueError: If task_term is an empty string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term cannot be empty.")
        term_lower = task_term.lower().strip()
        results = [
            task.copy() for task in self._tasks.values()
            if term_lower in task['task_name'].lower() or term_lower in task['task_description'].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished/completed.

        Args:
            task_id (int): The unique ID of the task to mark as finished.

        Returns:
            bool: True if the task was successfully marked as finished.

        Raises:
            ValueError: If task_id is negative or not an integer.
            KeyError: If a task with the given ID does not exist.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist.")

        self._tasks[task_id]['is_finished'] = True
        return True

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the manager.

        Returns:
            list[dict]: A list of all task dictionaries, each in the format:
                        {
                            'id': int,
                            'task_name': str,
                            'task_description': str,
                            'is_finished': bool
                        }
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the manager.

        Returns:
            bool: True if all tasks were successfully removed.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


def main():
    """
    Main function to run the console-based to-do list application.
    Provides a text-based menu for user interaction.
    """
    task_manager = TaskManager()

    instructions = (
        "\nTo-Do List Application Commands:\n"
        "  add       - Add a new task\n"
        "  remove    - Remove task by ID\n"
        "  finish    - Mark task as completed\n"
        "  search    - Search tasks by term\n"
        "  get_all   - List all tasks\n"
        "  clear_all - Delete all tasks\n"
        "  exit      - Exit the application\n"
    )
    print("Welcome to the Console-based To-Do List Application!")
    print(instructions)

    while True:
        command = input("Enter command: ").strip().lower()

        try:
            if command == "add":
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added with ID {task_id}.")

            elif command == "remove":
                task_id_input = input("Enter task ID to remove: ").strip()
                if not task_id_input.isdigit():
                    print("Invalid input. Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_input)
                task_manager.remove(task_id)
                print(f"Task with ID {task_id} has been removed.")

            elif command == "finish":
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                if not task_id_input.isdigit():
                    print("Invalid input. Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_input)
                task_manager.finish(task_id)
                print(f"Task with ID {task_id} marked as finished.")

            elif command == "search":
                term = input("Enter search term: ").strip()
                results = task_manager.search(term)
                if results:
                    print("Search Results:")
                    for task in results:
                        print(f"  ({task['id']}, {task['task_name']}, "
                              f"{task['task_description']}, Finished: {task['is_finished']})")
                else:
                    print("No tasks match the search term.")

            elif command == "get_all":
                tasks = task_manager.get_all()
                if tasks:
                    print("All Tasks:")
                    for task in tasks:
                        print(f"  ({task['id']}, {task['task_name']}, "
                              f"{task['task_description']}, Finished: {task['is_finished']})")
                else:
                    print("No tasks found.")

            elif command == "clear_all":
                confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirm == "yes":
                    task_manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear all canceled.")

            elif command == "exit":
                print("Exiting the application. Goodbye!")
                break

            else:
                print("Unknown command. Please try again.")
                print(instructions)

        except (ValueError, KeyError) as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
