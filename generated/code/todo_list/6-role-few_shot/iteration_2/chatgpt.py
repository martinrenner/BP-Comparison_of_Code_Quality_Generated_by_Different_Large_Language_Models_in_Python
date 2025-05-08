class TaskManager:
    """
    Manages tasks for a console-based to-do list application.

    Each task is stored as a dictionary with the following keys:
        - id: Unique task identifier.
        - task_name: The name of the task.
        - task_description: Details of the task.
        - is_finished: Boolean status indicating whether the task is completed.
    
    Tasks are stored in an in-memory dictionary for efficient lookup,
    insertion, and deletion.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task store and a task ID counter.
        """
        self.tasks = {}        # Dictionary mapping task IDs to task details.
        self.next_id = 1       # Next unique task ID to assign.

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description are empty.
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
        Removes the task with the given task ID.

        Args:
            task_id (int): The unique ID of the task.

        Returns:
            bool: True if the task was removed, False if not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Invalid task ID. Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks that contain the search term in their name or description.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of tasks (dictionaries) matching the search criteria.

        Raises:
            ValueError: If the search term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        results = [
            task for task in self.tasks.values()
            if term in task["task_name"].lower() or term in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks the task with the given task ID as finished.

        Args:
            task_id (int): The unique ID of the task.

        Returns:
            bool: True if the task was marked finished, False if not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Invalid task ID. Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks with their details.

        Returns:
            list[dict]: A list of all tasks, each formatted as:
                        {
                            "id": int,
                            "task_name": str,
                            "task_description": str,
                            "is_finished": bool
                        }
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            bool: True after all tasks have been cleared.
        """
        self.tasks.clear()
        return True


def main():
    """
    Runs a console-based to-do list application that allows users
    to add, remove, search, finish, view all, and clear tasks.
    """
    manager = TaskManager()

    COMMANDS = (
        "add, remove, search, finish, get_all, clear_all, exit"
    )
    print("Welcome to the Console To-Do List Application!")
    print(f"Available commands: {COMMANDS}")

    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == "add":
            try:
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = manager.add(name, description)
                print(f"Task added with ID {task_id}.")
            except ValueError as e:
                print(f"Error: {e}")

        elif command == "remove":
            try:
                task_id = int(input("Enter task ID to remove: "))
                if manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task with the given ID was not found.")
            except ValueError as e:
                print(f"Error: {e}")

        elif command == "search":
            try:
                term = input("Enter search term: ")
                results = manager.search(term)
                if results:
                    print("Matching tasks:")
                    for task in results:
                        print(task)
                else:
                    print("No matching tasks found.")
            except ValueError as e:
                print(f"Error: {e}")

        elif command == "finish":
            try:
                task_id = int(input("Enter task ID to mark as finished: "))
                if manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task with the given ID was not found.")
            except ValueError as e:
                print(f"Error: {e}")

        elif command == "get_all":
            tasks = manager.get_all()
            if tasks:
                print("All tasks:")
                for task in tasks:
                    print(task)
            else:
                print("No tasks available.")

        elif command == "clear_all":
            confirmation = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirmation == "yes":
                manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Clear all canceled.")

        elif command == "exit":
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Unknown command. Please try again.")
            print(f"Available commands: {COMMANDS}")


if __name__ == "__main__":
    main()
