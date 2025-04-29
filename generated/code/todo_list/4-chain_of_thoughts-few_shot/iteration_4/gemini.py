class TaskManager:
    """
    Manages a list of tasks, providing functionalities to add, remove,
    search, finish, retrieve, and clear tasks.  Implements an interface
    to interact with the todo list in an efficient, safe, and modular way.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and sets the
        initial ID counter to 1.
        """
        self.tasks = {}
        self.next_id = 1

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

        task_id = self.next_id
        self.tasks[task_id] = {
            "task_name": task_name,
            "task_description": task_description,
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
            return False

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks that contain the given term in their name or description.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of tasks (dictionaries) matching the search term.

        Raises:
            ValueError: If task_term is empty
        """

        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

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
            bool: True if the task was found and marked as finished, False otherwise.

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
            return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the task list.

        Returns:
            list[dict]: A list of all tasks, each represented as a dictionary.
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
        Removes all tasks from the task list.

        Returns:
            bool: Always returns True, indicating successful clearance.
        """
        self.tasks.clear()
        self.next_id = 1  # Resetting the ID counter
        return True


# Example usage demonstrating the functionality of TaskManager
if __name__ == "__main__":
    manager = TaskManager()

    # Add tasks
    try:
        id1 = manager.add("Grocery Shopping", "Buy milk, eggs, and bread")
        id2 = manager.add("Book Appointment", "Dentist appointment at 2 PM")
        print(f"Added tasks with IDs: {id1}, {id2}")
    except ValueError as e:
        print(f"Error adding tasks: {e}")

    # Get all tasks
    all_tasks = manager.get_all()
    print(f"All tasks: {all_tasks}")

    # Search for tasks
    try:
        search_results = manager.search("grocery")
        print(f"Search results for 'grocery': {search_results}")

        search_results = manager.search("appointment")
        print(f"Search results for 'appointment': {search_results}")

        search_results = manager.search("nonexistent")
        print(f"Search results for 'nonexistent': {search_results}")
    except ValueError as e:
         print(f"Error during search {e}")

    # Finish a task
    try:
        finished = manager.finish(id1)
        print(f"Task {id1} finished: {finished}")
        finished = manager.finish(999)  # Non-existent ID
        print(f"Task 999 finished: {finished}")
    except (TypeError, ValueError) as e:
        print(f"Error finishing task: {e}")


    # Get all tasks again (to see the updated status)
    all_tasks = manager.get_all()
    print(f"All tasks after finishing: {all_tasks}")

    # Remove a task
    try:
        removed = manager.remove(id2)
        print(f"Task {id2} removed: {removed}")
        removed = manager.remove(999)  # Non-existent ID
        print(f"Task 999 removed: {removed}")
    except (TypeError, ValueError) as e:
        print(f"Error removing task: {e}")

    # Get all tasks again (after removal)
    all_tasks = manager.get_all()
    print(f"All tasks after removal: {all_tasks}")

    # Clear all tasks
    cleared = manager.clear_all()
    print(f"All tasks cleared: {cleared}")

    # Get all tasks (should be empty)
    all_tasks = manager.get_all()
    print(f"All tasks after clearing: {all_tasks}")

     # Example of adding a task with invalid name
    try:
        invalid_id = manager.add("", "This task should not be added")
        print(f"Invalid task added with ID: {invalid_id}")  # Should not be reached
    except ValueError as e:
        print(f"Correctly handled error: {e}")

    # Test removing a task with non-integer ID
    try:
        manager.remove("abc")
    except TypeError as e:
        print(f"Correctly caught TypeError: {e}")

    # Test removing a task with negative ID
    try:
        manager.remove(-1)
    except ValueError as e:
        print(f"Correctly caught ValueError: {e}")

    # Test searching with empty search term:
    try:
        print(manager.search(""))
    except ValueError as e:
        print(f"Correctly caught ValueError: {e}")
