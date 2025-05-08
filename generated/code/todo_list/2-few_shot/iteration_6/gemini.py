class TaskManager:
    """
    Manages a list of tasks, allowing adding, removing, searching, finishing,
    retrieving, and clearing tasks.  This class adheres to ISO/IEC 25010
    standards by ensuring maintainability, reliability, usability,
    efficiency, and portability.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a unique ID counter.
        """
        self.tasks: list[dict] = []
        self.next_id: int = 1  # Start task IDs from 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the newly added task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task = {
            "id": self.next_id,
            "name": task_name,
            "description": task_description,
            "is_finished": False,
        }
        self.tasks.append(task)
        self.next_id += 1
        return task["id"]

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the task list by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was found and removed, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                del self.tasks[i]
                return True
        return False  # Task not found

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks by name or description.

        Args:
            task_term (str): The term to search for in task names and descriptions.

        Returns:
            list[dict]: A list of tasks that match the search term (case-insensitive).
                        Returns an empty list if no tasks match or if the search term is empty.

        Raises:
            ValueError: If the task search term is empty.
        """

        if not task_term.strip():
            raise ValueError("Task search term cannot be empty.")

        results: list[dict] = []
        for task in self.tasks:
            if task_term.lower() in task["name"].lower() or task_term.lower() in task[
                "description"
            ].lower():
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished, False otherwise.

        Raises:
             ValueError: If task_id is not a positive integer.
        """

        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        for task in self.tasks:
            if task["id"] == task_id:
                task["is_finished"] = True
                return True
        return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the list.

        Returns:
            list[dict]: A list of all tasks, including their ID, name, description, and completion status.
        """
        return self.tasks

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the Task Manager.

        Returns:
            bool: Always returns True, indicating that the task list has been cleared.
       """
        self.tasks = []
        return True
