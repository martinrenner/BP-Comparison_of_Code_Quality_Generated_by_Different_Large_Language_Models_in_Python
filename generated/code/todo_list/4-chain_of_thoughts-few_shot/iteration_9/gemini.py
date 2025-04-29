class TaskManager:
    """
    Manages a to-do list with add, remove, search, finish, get_all, and clear_all functionalities.

    This class uses a dictionary to store tasks, providing efficient lookups, insertions, and deletions.
    It adheres to principles of OOP, error handling, and input validation.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and sets the next available ID to 1.
        """
        self.tasks = {}
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the newly added task.

        Raises:
            ValueError: If either task_name or task_description is empty.
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
        Searches for tasks matching a given term in their name or description.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of matching tasks.  Each task is a dictionary
                         with keys 'id', 'name', 'description', and 'is_finished'.

        Raises:
            ValueError: If the search term is empty.
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
            bool: True if the task was found and marked as finished, False otherwise.

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
            list[dict]: A list of all tasks. Each task is a dictionary
                         with keys 'id', 'name', 'description', and 'is_finished'.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Clears all tasks from the to-do list.

        Returns:
            bool: Always returns True, indicating successful clearance.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset ID counter
        return True


if __name__ == "__main__":
    # Create a TaskManager instance
    manager = TaskManager()

    # Add some tasks
    try:
        id1 = manager.add("Grocery Shopping", "Buy milk, eggs, and bread.")
        id2 = manager.add("Book Appointment", "Schedule a doctor's appointment.")
        print(f"Added tasks with IDs: {id1}, {id2}")
    except ValueError as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    all_tasks = manager.get_all()
    print("All Tasks:", all_tasks)

    # Search for tasks
    try:
        search_results = manager.search("appointment")
        print("Search Results:", search_results)
    except ValueError as e:
        print(f"Error searching: {e}")

    # Finish a task
    try:
        finished = manager.finish(id1)
        print(f"Task {id1} finished: {finished}")
    except (TypeError, ValueError) as e:
        print(f"Error finishing: {e}")

    # Remove a task
    try:
        removed = manager.remove(id2)
        print(f"Task {id2} removed: {removed}")
    except (TypeError, ValueError) as e:
        print(f"Error removing: {e}")

    # Try removing a non-existent task
    try:
        removed = manager.remove(999)
        print(f"Task 999 removed: {removed}") # Should be false
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")

    # Get all tasks again (should be only one, finished task)
    all_tasks = manager.get_all()
    print("All Tasks after finishing and removing:", all_tasks)

    #Clear all
    manager.clear_all()
    print("Clear all", manager.get_all())

    # Example of adding an empty string, catching the error
    try:
        id_error = manager.add("", "")
    except ValueError as e:
        print(f"Caught Expected Error: {e}")

    # Example of finishing wrong id, catching the error
    try:
        manager.finish(0.5)
    except TypeError as e:
        print(f"Caught Expected Error: {e}")
