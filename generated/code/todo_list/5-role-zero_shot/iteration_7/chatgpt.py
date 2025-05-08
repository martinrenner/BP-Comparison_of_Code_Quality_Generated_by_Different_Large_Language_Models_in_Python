class TaskManager:
    """
    TaskManager handles a console-based to-do list.
    It provides operations to add, remove, search, finish, retrieve, and clear tasks.
    Each task is stored as a dictionary with keys:
        - id: Unique identifier of the task.
        - task_name: Name of the task.
        - task_description: Detailed description of the task.
        - is_finished: Boolean flag indicating task completion.
    """

    def __init__(self):
        # In-memory storage for tasks (dict for efficient O(1) lookups, insertions, deletions)
        self._tasks = {}  # Maps task_id -> task (dict)
        self._next_id = 1  # Counter for generating unique task IDs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name (str): The name of the task. Must be a non-empty string.
            task_description (str): The description of the task. Must be a non-empty string.

        Returns:
            int: The unique identifier assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is empty or not a string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self._next_id
        # Store the task details in a dictionary.
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self._next_id += 1  # Increment the unique ID counter
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique identifier.

        Args:
            task_id (int): The ID of the task to remove. Must be a positive integer.

        Returns:
            bool: True if the task was successfully removed, False if the task doesn't exist.

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
        Searches for tasks by matching a substring in the task name or description.

        Args:
            task_term (str): The search term (case-insensitive). Must be a non-empty string.

        Returns:
            list: A list of tasks (each task is a dict) that match the search criteria.

        Raises:
            ValueError: If task_term is not a non-empty string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        results = [
            task for task in self._tasks.values()
            if term in task["task_name"].lower() or term in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The unique identifier of the task to mark as finished.
                           Must be a positive integer.

        Returns:
            bool: True if the task exists and was marked as finished,
                  False if the task does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            self._tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all tasks.

        Returns:
            list: A list of all tasks (each represented as a dict) sorted by task ID.
        """
        # Sorting tasks by their ID in ascending order
        return sorted(self._tasks.values(), key=lambda task: task["id"])

    def clear_all(self) -> bool:
        """
        Clears all tasks from the to-do list.

        Returns:
            bool: True after all tasks have been successfully cleared.
        """
        self._tasks.clear()
        return True


def run_console():
    """
    Runs the console-based loop for the to-do list application.
    Provides a simple text-based menu for user interaction.
    """
    task_manager = TaskManager()
    menu = """
Console To-Do List Application:
1. Add Task
2. Remove Task
3. Search Tasks
4. Mark Task as Finished
5. Get All Tasks
6. Clear All Tasks
7. Exit
"""
    while True:
        print(menu)
        choice = input("Enter an option (1-7): ").strip()
        if choice == '1':
            try:
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as e:
                print("Error:", e)

        elif choice == '2':
            try:
                task_id_input = input("Enter task ID to remove: ").strip()
                task_id = int(task_id_input)
                if task_manager.remove(task_id):
                    print(f"Task {task_id} removed successfully.")
                else:
                    print(f"Task with ID {task_id} does not exist.")
            except ValueError as e:
                print("Error:", e)

        elif choice == '3':
            try:
                term = input("Enter search term: ").strip()
                results = task_manager.search(term)
                if results:
                    print("Search Results:")
                    for task in results:
                        status = "Finished" if task["is_finished"] else "Pending"
                        print(f"ID: {task['id']} | Name: {task['task_name']} | Description: {task['task_description']} | Status: {status}")
                else:
                    print("No tasks found matching the search criteria.")
            except ValueError as e:
                print("Error:", e)

        elif choice == '4':
            try:
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                task_id = int(task_id_input)
                if task_manager.finish(task_id):
                    print(f"Task {task_id} marked as finished.")
                else:
                    print(f"Task with ID {task_id} does not exist.")
            except ValueError as e:
                print("Error:", e)

        elif choice == '5':
            tasks = task_manager.get_all()
            if tasks:
                print("All Tasks:")
                for task in tasks:
                    status = "Finished" if task["is_finished"] else "Pending"
                    print(f"ID: {task['id']} | Name: {task['task_name']} | Description: {task['task_description']} | Status: {status}")
            else:
                print("No tasks to display.")

        elif choice == '6':
            confirm = input("Are you sure you want to clear all tasks? (y/N): ").strip().lower()
            if confirm == 'y':
                task_manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Operation cancelled.")

        elif choice == '7':
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid option. Please choose a number between 1 and 7.")


if __name__ == "__main__":
    run_console()
