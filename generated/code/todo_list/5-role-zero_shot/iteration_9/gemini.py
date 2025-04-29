class TaskManager:
    """
    Manages a to-do list with functionalities to add, remove, search,
    finish, get all tasks, and clear all tasks.  Implements an in-memory
    storage using a dictionary for efficient lookups.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a counter for task IDs.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups by ID. {id: Task}
        self.next_task_id = 1  # Counter to assign unique IDs.

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name: The name of the task (cannot be empty).
            task_description: A description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            ValueError: If task_name is empty.
        """
        if not task_name:
            raise ValueError("Task name cannot be empty.")

        task_id = self.next_task_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
        }
        self.next_task_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the to-do list by its ID.

        Args:
            task_id: The ID of the task to be removed.

        Returns:
            True if the task was successfully removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not positive.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        else:
            return False  # Task not found

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks by name or description.

        Args:
            task_term: The search term (can be part of the name or description).

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if no matches are found.

        Raises:
            ValueError: if the task_term is empty
        """
        if not task_term:
            raise ValueError("Search term cannot be empty.")

        results = []
        for task_id, task_data in self.tasks.items():
            if (
                task_term.lower() in task_data["task_name"].lower()
                or task_term.lower() in task_data["task_description"].lower()
            ):
                results.append(task_data)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to be marked as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not positive.
        """

        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        else:
            return False  # Task not found

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the to-do list.

        Returns:
            A list of dictionaries, where each dictionary represents a task
            (including ID, name, description, and completion status).
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the to-do list.

        Returns:
            Always returns True, indicating that the list has been cleared.
        """
        self.tasks.clear()
        self.next_task_id = 1  # Reset the ID counter
        return True

