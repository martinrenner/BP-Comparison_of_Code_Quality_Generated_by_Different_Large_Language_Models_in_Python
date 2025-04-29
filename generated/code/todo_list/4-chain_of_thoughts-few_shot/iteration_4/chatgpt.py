class TaskManager:
    """
    A TaskManager for managing tasks in a console-based todo list application.

    Each task is stored as a dictionary with the following keys:
    - id (int): Unique identifier of the task.
    - task_name (str): The name/title of the task.
    - task_description (str): Details about the task.
    - is_finished (bool): Status indicating whether the task is completed.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task storage and a counter for unique IDs.
        """
        self._tasks = {}  # Dictionary to store tasks keyed by task id for O(1) operations.
        self._next_id = 1  # Unique incremental ID generator for tasks.

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task with the given name and description.

        Args:
            task_name (str): The name of the task. Must be a non-empty string.
            task_description (str): The description of the task. Must be a non-empty string.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id (int): The unique ID of the task to remove. Must be a positive integer.

        Returns:
            bool: True if the task was successfully removed.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If no task exists for the provided ID.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist.")

        del self._tasks[task_id]
        return True

    def search(self, task_term: str) -> list:
        """
        Searches for tasks that contain the search term in their name or description (case-insensitive).

        Args:
            task_term (str): The term to search for. Must be a non-empty string.

        Returns:
            list[dict]: A list of tasks matching the search criteria. Each task is represented as a dictionary.

        Raises:
            ValueError: If task_term is an empty string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        results = []
        for task in self._tasks.values():
            if term in task["task_name"].lower() or term in task["task_description"].lower():
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished (completed) by its ID.

        Args:
            task_id (int): The unique ID of the task to mark as finished.
                           Must be a positive integer.

        Returns:
            bool: True if the task status was successfully updated.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If no task exists for the provided ID.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist.")

        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> list:
        """
        Retrieves all tasks with their full details.

        Returns:
            list[dict]: A list of all tasks stored, each task represented as a dictionary.
        """
        # Sorting tasks by their ID for consistent ordering.
        return [self._tasks[task_id] for task_id in sorted(self._tasks.keys())]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the task manager.

        Returns:
            bool: True after all tasks have been cleared.
        """
        self._tasks.clear()
        return True


def display_task(task: dict) -> None:
    """
    Displays a task in a readable format.

    Args:
        task (dict): A task dictionary containing id, task_name, task_description, and is_finished.
    """
    status = "Finished" if task.get("is_finished") else "Pending"
    print(f"(ID: {task.get('id')}) {task.get('task_name')}: {task.get('task_description')} [{status}]")


def print_menu() -> None:
    """
    Prints the main menu options.
    """
    print("\n--- Todo List Menu ---")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Search Tasks")
    print("4. Mark Task as Finished")
    print("5. Get All Tasks")
    print("6. Clear All Tasks")
    print("7. Exit\n")


def main():
    """
    The main function to run the console-based todo list application.
    """
    task_manager = TaskManager()
    print("Welcome to the Console-based Todo List App!")
    
    while True:
        print_menu()
        choice = input("Select an option (1-7): ").strip()
        
        try:
            if choice == "1":
                # Add Task
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")

            elif choice == "2":
                # Remove Task
                id_input = input("Enter the task ID to remove: ").strip()
                task_id = int(id_input)
                task_manager.remove(task_id)
                print(f"Task with ID {task_id} removed successfully.")

            elif choice == "3":
                # Search Tasks
                term = input("Enter search term: ").strip()
                results = task_manager.search(term)
                if results:
                    print("Matching Tasks:")
                    for task in results:
                        display_task(task)
                else:
                    print("No matching tasks found.")

            elif choice == "4":
                # Mark Task as Finished
                id_input = input("Enter the task ID to mark as finished: ").strip()
                task_id = int(id_input)
                task_manager.finish(task_id)
                print(f"Task with ID {task_id} marked as finished.")

            elif choice == "5":
                # Get All Tasks
                tasks = task_manager.get_all()
                if tasks:
                    print("All Tasks:")
                    for task in tasks:
                        display_task(task)
                else:
                    print("No tasks available.")

            elif choice == "6":
                # Clear All Tasks
                confirmation = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirmation == "yes":
                    task_manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear all tasks cancelled.")

            elif choice == "7":
                print("Exiting the Todo List App. Goodbye!")
                break

            else:
                print("Invalid option. Please select a number between 1 and 7.")

        except ValueError as ve:
            print(f"Input error: {ve}")
        except KeyError as ke:
            print(f"Task error: {ke}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
