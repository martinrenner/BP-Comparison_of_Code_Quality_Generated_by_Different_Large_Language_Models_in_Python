class TaskManager:
    """
    Manages a list of tasks, allowing adding, removing, searching,
    finishing, retrieving, and clearing tasks.  Implements in-memory
    storage and prioritizes efficiency and error handling.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and sets the
        initial task ID to 1.
        """
        self.tasks = {}  # Dictionary to store tasks: {task_id: task_details}
        self.next_task_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_task_id
        self.tasks[task_id] = {
            "id": task_id,
            "name": task_name,
            "description": task_description,
            "is_finished": False,
        }
        self.next_task_id += 1
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
            ValueError: If task_id is negative or zero.
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
            task_term (str): The term to search for (in name or description).

        Returns:
            list[dict]: A list of matching tasks (empty list if no matches).

        Raises:
            ValueError: If search term is an empty string or only whitespace.
        """

        if not task_term.strip():  # Check that task_term contains at least one non-whitespace character
            raise ValueError("Search term cannot be empty.")

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
            bool: True if the task was found and marked as finished,
                  False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
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
        Retrieves all tasks.

        Returns:
            list[dict]: A list of all tasks.  Each task is a dictionary.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: Always returns True, indicating successful clearance.
        """
        self.tasks.clear()
        self.next_task_id = 1  # Reset ID counter
        return True


# Example Usage
if __name__ == "__main__":
    tm = TaskManager()

    # Add tasks
    task1_id = tm.add("Grocery Shopping", "Buy milk, eggs, bread, and cheese.")
    task2_id = tm.add("Book Appointment", "Schedule a doctor's appointment.")
    task3_id = tm.add("Pay Bills", "Pay electricity and water bills.")

    # Get all tasks
    all_tasks = tm.get_all()
    print("All Tasks:", all_tasks)


    # Search for tasks
    search_results = tm.search("appointment")
    print("Search Results (appointment):", search_results)

    search_results = tm.search("buy")
    print("Search Results (buy):", search_results)

    # Finish a task
    tm.finish(task1_id)
    print("All Tasks After Finishing ID 1:", tm.get_all())

    # Remove a task
    tm.remove(task2_id)
    print("All Tasks After Removing ID 2:", tm.get_all())

    # Clear all tasks
    tm.clear_all()
    print(f"Check that all tasks were deleted: {tm.get_all()}")

    # Demonstrate error handling (uncomment each to test)

    # try:
    #     tm.add("", "Description")  # Empty task name
    # except ValueError as e:
    #     print(f"Error caught as expected: {e}")

    # try:
    #     tm.add("Task Name", "")  # Empty description
    # except ValueError as e:
    #     print(f"Error caught as expected: {e}")

    # try:
    #     tm.remove(-1)  # Negative ID
    # except ValueError as e:
    #     print(f"Error caught as expected: {e}")

    # try:
    #     tm.remove(5) # Try to remove non-existent ID
    # except ValueError as e:
    #     print(f"Error caught as expected: {e}")

    # try:
    #       tm.remove(2.5)  # Invalid task ID
    # except TypeError as e:
    #     print(f"Error caught as expected: {e}")

    # try:
    #     tm.search("   ") # search empty string
    # except ValueError as e:
    #     print(f"Error caught as expected: {e}")
