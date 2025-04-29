class TaskManager:
    """
    Manages a list of tasks in a console-based to-do list application.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a task ID counter.
        """
        self.tasks = {}  # Dictionary to store tasks: {task_id: {task_details}}
        self.next_id = 1  # Counter for generating unique task IDs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description are empty strings.
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
        Removes a task from the to-do list by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        else:
            return False  # Task not found

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks matching a given term (in name or description).

        Args:
            task_term (str): The search term.

        Returns:
            list[dict]: A list of dictionaries, each representing a matching task.
                        Returns an empty list if no tasks match.

        Raises:
            ValueError: If task_term is empty
        """

        if not task_term.strip():
            raise ValueError("Search term cannot be empty")

        results = []
        for task_id, task_details in self.tasks.items():
            if (
                task_term.lower() in task_details["name"].lower()
                or task_term.lower() in task_details["description"].lower()
            ):
                results.append(task_details)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was successfully marked as finished,
                  False otherwise (e.g., task not found).

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        else:
            return False  # Task not found

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the to-do list.

        Returns:
            list[dict]: A list of dictionaries, each representing a task.
                        Returns an empty list if there are no tasks.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the to-do list.

        Returns:
            bool: Always returns True, indicating success.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset ID counter
        return True


# Create a TaskManager instance
if __name__ == "__main__":
    manager = TaskManager()

    # Add tasks
    try:
        id1 = manager.add("Grocery Shopping", "Buy milk, eggs, and bread")
        id2 = manager.add("Book Appointment", "Schedule a doctor's appointment")
        print(f"Added tasks with IDs: {id1}, {id2}")
    except ValueError as e:
        print(f"Error: {e}")

    # Get all tasks
    all_tasks = manager.get_all()
    print("All tasks:", all_tasks)

    # Search for tasks
    try:
        search_results = manager.search("appointment")
        print("Search results:", search_results)
    except ValueError as e:
        print(f"Error {e}")

    # Finish a task
    try:
        finished = manager.finish(id1)
        print(f"Task {id1} finished:", finished)
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")


    # Remove a task
    try:
        removed = manager.remove(id2)
        print(f"Task {id2} removed:", removed)
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")

    # Get all tasks again (after finishing and removing)
    all_tasks = manager.get_all()
    print("All tasks after updates:", all_tasks)

    # Try to remove a non-existent task
    try:
        removed = manager.remove(999)
        print(f"Task 999 removed:", removed)  # Should print False
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")

    # Clear all tasks
    cleared = manager.clear_all()
    print("Cleared all tasks:", cleared)

    # Get all tasks (should be empty)
    all_tasks = manager.get_all()
    print("All tasks after clearing:", all_tasks)  # Should print []

    # Test adding task with empty name
    try:
        manager.add("", "This should raise an exception")  # Empty task name
    except ValueError as e:
        print(f"Expected error (empty task name): {e}")

    # Test finish a task with non-integer id
    try:
        manager.finish("five")
    except TypeError as e:
        print(f"Expected error (non-integer id): {e}")

    # Test removing a task with negative id
    try:
        manager.remove(-1)
    except ValueError as e:
        print(f"Expected error (negative id): {e}")
    # Test searching with an empty string:
    try:
        manager.search("")
    except ValueError as e:
        print(f"Expected error (empty search term): {e}")
