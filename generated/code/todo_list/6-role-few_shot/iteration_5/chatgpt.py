class TaskManager:
    """
    A task manager for a console-based to-do list application.
    This class allows adding, removing, searching, marking tasks as finished,
    retrieving all tasks, and clearing all tasks.
    
    Each task is represented as a dictionary with the following keys:
        - id (int): A unique task identifier.
        - task_name (str): The name of the task.
        - task_description (str): A description of the task.
        - is_finished (bool): The completion status of the task.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty collection of tasks and
        sets the initial unique ID counter to 1.
        """
        self._tasks = {}  # Mapping from task ID to task details.
        self._next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.
        
        Args:
            task_name (str): The name of the task. Must be non-empty.
            task_description (str): The description of the task. Must be non-empty.
            
        Returns:
            int: The unique ID assigned to the new task.
            
        Raises:
            ValueError: If either task_name or task_description is an empty string.
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
        Removes a task by its unique ID.
        
        Args:
            task_id (int): The unique ID of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False if the task does not exist.
            
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

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks with names or descriptions containing the provided term.
        The search is case-insensitive.
        
        Args:
            task_term (str): The term to search for in task names or descriptions.
            
        Returns:
            list[dict]: A list of tasks (as dictionaries) that match the search criteria.
            
        Raises:
            ValueError: If task_term is not a non-empty string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.lower().strip()
        matching_tasks = []
        for task in self._tasks.values():
            if term in task["task_name"].lower() or term in task["task_description"].lower():
                # Append a copy of the task dictionary to avoid external mutation.
                matching_tasks.append(task.copy())
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks the task with the given ID as finished.
        
        Args:
            task_id (int): The unique ID of the task to mark as finished.
            
        Returns:
            bool: True if the task was found and updated, False if the task does not exist.
            
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

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the to-do list.
        
        Returns:
            list[dict]: A list of all tasks, where each task is represented as a dictionary
            with keys (id, task_name, task_description, is_finished).
        """
        # Returning tasks sorted by their ID for consistency.
        return [task.copy() for task in sorted(self._tasks.values(), key=lambda x: x["id"])]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the to-do list.
        
        Returns:
            bool: True after clearing all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


def main() -> None:
    """
    The main loop for the console-based to-do list application.
    Handles user input and maps commands to the TaskManager methods.
    """
    task_manager = TaskManager()
    menu = (
        "\nPlease choose a command:\n"
        "1. add       - Add a new task\n"
        "2. remove    - Remove a task by its ID\n"
        "3. search    - Search tasks by a term\n"
        "4. finish    - Mark a task as finished\n"
        "5. get_all   - List all tasks\n"
        "6. clear_all - Clear all tasks\n"
        "7. exit      - Exit the application\n"
        "Enter your choice: "
    )

    print("Welcome to the To-Do List Application!")
    while True:
        try:
            command = input(menu).strip().lower()
            if command in {"7", "exit"}:
                print("Exiting the application. Goodbye!")
                break

            if command in {"1", "add"}:
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                new_id = task_manager.add(task_name, task_description)
                print(f"Task added with ID: {new_id}")

            elif command in {"2", "remove"}:
                try:
                    task_id = int(input("Enter task ID to remove: ").strip())
                    if task_manager.remove(task_id):
                        print(f"Task with ID {task_id} removed successfully.")
                    else:
                        print(f"No task found with ID {task_id}.")
                except ValueError:
                    print("Invalid input. Please enter a valid integer for task ID.")

            elif command in {"3", "search"}:
                term = input("Enter search term: ")
                matching_tasks = task_manager.search(term)
                if matching_tasks:
                    print("Matching Tasks:")
                    for task in matching_tasks:
                        print(task)
                else:
                    print("No tasks matched your search term.")

            elif command in {"4", "finish"}:
                try:
                    task_id = int(input("Enter task ID to mark as finished: ").strip())
                    if task_manager.finish(task_id):
                        print(f"Task with ID {task_id} marked as finished.")
                    else:
                        print(f"No task found with ID {task_id}.")
                except ValueError:
                    print("Invalid input. Please enter a valid integer for task ID.")

            elif command in {"5", "get_all"}:
                tasks = task_manager.get_all()
                if tasks:
                    print("All Tasks:")
                    for task in tasks:
                        print(task)
                else:
                    print("There are no tasks to display.")

            elif command in {"6", "clear_all"}:
                confirmation = input("Are you sure you want to remove all tasks? (yes/no): ").strip().lower()
                if confirmation == "yes":
                    task_manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear all tasks canceled.")

            else:
                print("Unrecognized command. Please try again.")

        except Exception as e:
            # Display any unexpected errors gracefully.
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
