from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union


class TaskManager:
    """
    Manages a to-do list with various operations like adding, removing, searching,
    and tracking task completion status.

    Attributes:
        _tasks (Dict[int, Dict]): Dictionary storing tasks with task ID as key.
        _next_id (int): The next available ID for new tasks.
    """

    def __init__(self):
        """Initialize an empty task manager with a counter for task IDs."""
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the to-do list.

        Args:
            task_name (str): The name of the task.
            task_description (str): The detailed description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        # Validate inputs
        if not task_name.strip():
            raise ValueError("Task name cannot be empty")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty")

        # Create task
        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False,
            "created_at": datetime.now()
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the to-do list by its ID.

        Args:
            task_id (int): The unique identifier of the task to be removed.

        Returns:
            bool: True if the task was successfully removed, False otherwise.

        Raises:
            ValueError: If task_id is negative or zero.
        """
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description that contain the specified term.

        Args:
            task_term (str): The search term to look for in task names or descriptions.

        Returns:
            List[Dict]: A list of task dictionaries matching the search criteria.

        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty")

        search_term = task_term.lower().strip()
        results = []

        for task in self._tasks.values():
            if (search_term in task["task_name"].lower() or
                    search_term in task["task_description"].lower()):
                results.append(self._format_task_output(task))
        
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed by its ID.

        Args:
            task_id (int): The unique identifier of the task to mark as completed.

        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.

        Raises:
            ValueError: If task_id is negative or zero.
        """
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if task_id in self._tasks:
            task = self._tasks[task_id]
            if task["is_finished"]:
                return False  # Task already finished
            task["is_finished"] = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks in the to-do list.

        Returns:
            List[Dict]: A list of all task dictionaries.
        """
        return [self._format_task_output(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Delete all tasks from the to-do list.

        Returns:
            bool: True if all tasks were successfully cleared.
        """
        self._tasks.clear()
        return True

    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format a task dictionary for output according to the required format.

        Args:
            task (Dict): The task dictionary to format.

        Returns:
            Dict: A dictionary containing only the required task fields.
        """
        return {
            "id": task["id"],
            "task_name": task["task_name"],
            "task_description": task["task_description"],
            "is_finished": task["is_finished"]
        }
