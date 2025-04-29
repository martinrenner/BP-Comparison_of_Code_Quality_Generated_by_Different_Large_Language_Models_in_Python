class TaskManager:
    """
    Manages a list of tasks, allowing for adding, removing, searching,
    finishing, retrieving, and clearing tasks.  This class adheres to
    ISO/IEC 25010 standards by focusing on functional correctness,
    performance efficiency, maintainability, security, and testability.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a starting ID.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups by ID
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task list.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID assigned to the newly added task.

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
            "name": task_name,
            "description": task_description,
            "is_finished": False,
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the task list by its ID.

        Args:
            task_id (int): The ID of the task to be removed.

        Returns:
            bool: True if the task was successfully removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not an integer
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks that contain the given term in their name or description.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of tasks that match the search term.  Empty list
                        if no matches are found.

        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        results = []
        for task in self.tasks.values():
            if task_term.lower() in task["name"].lower() or task_term.lower() in task["description"].lower():
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished,
                  False otherwise.
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not an integer
        """

        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the task list.

        Returns:
            list[dict]: A list of all tasks, with each task represented as a dictionary
                    containing 'id', 'name', 'description', and 'is_finished'.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Removes all tasks from the task list.

        Returns:
            bool: Always returns True, indicating successful clearance of tasks.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset the ID counter
        return True
