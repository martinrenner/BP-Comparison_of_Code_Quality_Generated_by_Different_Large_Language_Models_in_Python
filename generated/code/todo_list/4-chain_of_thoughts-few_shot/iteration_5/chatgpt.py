class TaskManager:
    """
    A class to manage tasks in a console-based todo list application.

    This class implements the following functions:
      - add(task_name: str, task_description: str) -> int
      - remove(task_id: int) -> bool
      - search(task_term: str) -> list[dict]
      - finish(task_id: int) -> bool
      - get_all() -> list[dict]
      - clear_all() -> bool

    Each task is stored as a dictionary containing:
      (id, task_name, task_description, is_finished)
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty in-memory data structure and a task counter.
        """
        self.tasks = {}  # Using a dict for efficient lookup, insertion, and deletion.
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task list.

        Args:
            task_name (str): The name of the task (must not be empty).
            task_description (str): The description of the task (must not be empty).

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes an existing task by its ID.

        Args:
            task_id (int): The unique ID of the task to remove (must be a positive integer).

        Returns:
            bool: True if the task was removed successfully, False if the task was not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Searches for tasks that contain the given term in their name or description (case-insensitive).

        Args:
            task_term (str): The term to search for (must not be empty).

        Returns:
            list[dict]: A list of tasks (as dictionaries) that match the search criteria.

        Raises:
            ValueError: If task_term is an empty string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = task_term.strip().lower()
        result = []
        for task in self.tasks.values():
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower():
                result.append(task)
        return result

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The unique ID of the task to mark as finished (must be a positive integer).

        Returns:
            bool: True if the task was marked as finished, False if the task was not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all tasks in the todo list.

        Returns:
            list[dict]: A list of all tasks with their details.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Removes all tasks from the todo list.

        Returns:
            bool: True once all tasks have been cleared.
        """
        self.tasks.clear()
        return True


def main():
    """
    Runs the console-based todo list application.
    
    The user is presented with options to add, remove, search, finish tasks,
    get all tasks, clear all tasks, or exit the application.
    """
    manager = TaskManager()
    print("Welcome to the Todo List App!")

    menu = (
        "\nAvailable Commands:\n"
        "1. add        - Add a new task\n"
        "2. remove     - Remove a task by ID\n"
        "3. search     - Search tasks by term\n"
        "4. finish     - Mark a task as finished\n"
        "5. get_all    - List all tasks\n"
        "6. clear_all  - Clear all tasks\n"
        "7. exit       - Exit the application\n"
    )

    while True:
        print(menu)
        command = input("Enter command: ").strip().lower()

        if command in ("add", "1"):
            try:
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = manager.add(name, description)
                print(f"Task added with ID: {task_id}")
            except ValueError as ve:
                print("Error:", ve)

        elif command in ("remove", "2"):
            try:
                task_id_str = input("Enter task ID to remove: ").strip()
                task_id = int(task_id_str)
                if manager.remove(task_id):
                    print(f"Task {task_id} removed successfully.")
                else:
                    print(f"No task found with ID: {task_id}")
            except ValueError:
                print("Error: Please enter a valid positive integer for task ID.")

        elif command in ("search", "3"):
            try:
                term = input("Enter search term: ").strip()
                results = manager.search(term)
                if results:
                    print("Matching Tasks:")
                    for task in results:
                        # Display task in the format: (id, task_name, task_description, is_finished)
                        print((task["id"], task["task_name"], task["task_description"], task["is_finished"]))
                else:
                    print("No tasks match the search term.")
            except ValueError as ve:
                print("Error:", ve)

        elif command in ("finish", "4"):
            try:
                task_id_str = input("Enter task ID to mark as finished: ").strip()
                task_id = int(task_id_str)
                if manager.finish(task_id):
                    print(f"Task {task_id} marked as finished.")
                else:
                    print(f"No task found with ID: {task_id}")
            except ValueError:
                print("Error: Please enter a valid positive integer for task ID.")

        elif command in ("get_all", "5"):
            all_tasks = manager.get_all()
            if all_tasks:
                print("All Tasks:")
                for task in all_tasks:
                    print((task["id"], task["task_name"], task["task_description"], task["is_finished"]))
            else:
                print("No tasks available.")

        elif command in ("clear_all", "6"):
            confirmation = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirmation == "yes":
                manager.clear_all()
                print("All tasks cleared.")
            else:
                print("Clear operation cancelled.")

        elif command in ("exit", "7"):
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
