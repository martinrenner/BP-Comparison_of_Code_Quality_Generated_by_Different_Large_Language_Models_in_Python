class TaskManager:
    """
    Manages a list of tasks.  Provides functionality to add, remove,
    search, finish, and retrieve tasks.  Uses in-memory storage.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and an ID counter.
        """
        self.tasks = {}  # Dictionary to store tasks: {task_id: {task_details}}
        self._id_counter = 1  # Counter to generate unique task IDs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If the task_name is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        task_id = self._id_counter
        self.tasks[task_id] = {
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
        }
        self._id_counter += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the list by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        else:
            return False

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks by name or description.

        Args:
            task_term (str): The term to search for (case-insensitive).

        Returns:
            list[dict]: A list of matching tasks.  Each task is represented
                        as a dictionary: {id, task_name, task_description, is_finished}.
                        Returns an empty list if no matches are found.
        Raises:
            ValueError: If search term is empty
        """
        if not task_term.strip():
            raise ValueError("Search term should not be empty")

        results = []
        for task_id, task_details in self.tasks.items():
            if (
                task_term.lower() in task_details["task_name"].lower()
                or task_term.lower() in task_details["task_description"].lower()
            ):
                results.append(
                    {
                        "id": task_id,
                        "task_name": task_details["task_name"],
                        "task_description": task_details["task_description"],
                        "is_finished": task_details["is_finished"],
                    }
                )
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
            TypeError: If task_id is not an integer.
            ValueError: If task negative.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        else:
            return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: A list of all tasks. Each task is a dictionary:
                        {id, task_name, task_description, is_finished}.
        """
        return [
            {
                "id": task_id,
                "task_name": task_details["task_name"],
                "task_description": task_details["task_description"],
                "is_finished": task_details["is_finished"],
            }
            for task_id, task_details in self.tasks.items()
        ]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the list.

        Returns:
            bool: Always returns True (for consistency).
        """
        self.tasks.clear()
        self._id_counter = 1  # Reset the ID counter
        return True


# Example Usage (for demonstration - not part of the class)
if __name__ == "__main__":
    manager = TaskManager()

    # Add tasks
    try:
        id1 = manager.add("Grocery Shopping", "Buy milk, eggs, and bread")
        id2 = manager.add("Book Doctor Appointment", "For annual checkup")
        print(f"Added task with ID: {id1}")
        print(f"Added task with ID: {id2}")
    except ValueError as e:
        print(f"Error: {e}")

    # Get all tasks
    all_tasks = manager.get_all()
    print("All Tasks:", all_tasks)

    # Search for tasks
    try:
        search_results = manager.search("doctor")
        print("Search Results:", search_results)

        search_results = manager.search("invalid task")
        print("Search Results:", search_results)
    except ValueError as e:
        print(f"Error: {e}")


    # Finish a task
    if manager.finish(id1):
        print(f"Task {id1} marked as finished.")
    else:
        print(f"Task {id1} not found.")

    # Remove a task
    if manager.remove(id2):
        print(f"Task {id2} removed.")
    else:
        print(f"Task {id2} not found.")

    # Try to remove a non-existent task
    if manager.remove(999):
        print("Task 999 removed (should not happen).")
    else:
        print("Task 999 not found (expected).")

    # Get all tasks again (after finishing and removing)
    all_tasks = manager.get_all()
    print("All Tasks (after updates):", all_tasks)

    # Clear all tasks
    manager.clear_all()
    print("All tasks cleared.  Current tasks:", manager.get_all())

    try:
        manager.add("", "test")
    except ValueError as e:
        print(f"Error: {e}")

    try:
        manager.remove(-1)
    except ValueError as e:
        print(f"Error {e}")

    try:
        manager.remove(1.1)
    except TypeError as e:
        print(f"Error {e}")

    try:
        manager.search("")
    except ValueError as e:
        print(f"Error: {e}")
