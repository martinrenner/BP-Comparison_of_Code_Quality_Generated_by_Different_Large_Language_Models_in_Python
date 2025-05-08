class TaskManager:
    """
    Manages a to-do list, allowing users to add, remove, search,
    finish, and view tasks.  Tasks are stored in-memory.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and sets the
        next available task ID to 1.
        """
        self.tasks = {}  # Dictionary to store tasks: {task_id: task_details}
        self.next_id = 1

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
            ValueError: If task_id is not a positive integer.
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
            task_term (str): The search term (can be part of the name or description).

        Returns:
            list[dict]: A list of matching tasks.  Each task is a dictionary
                        containing 'id', 'name', 'description', and 'is_finished'.
                        Returns an empty list if no tasks match.

        Raises:
            ValueError: If task_term is an empty string.
        """

        if not task_term.strip():
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
            ValueError: If task_id is not a positive integer.
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
            list[dict]: A list of all tasks.  Each task is a dictionary
                        containing 'id', 'name', 'description', and 'is_finished'.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the to-do list.

        Returns:
            bool: Always returns True, indicating that the list was cleared.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset ID counter
        return True


# Example usage and basic testing
if __name__ == "__main__":
    tm = TaskManager()

    # Add tasks
    try:
        id1 = tm.add("Grocery Shopping", "Buy milk, eggs, and bread.")
        id2 = tm.add("Book Doctor Appointment", "Schedule checkup for next week.")
        print(f"Added tasks with IDs: {id1}, {id2}")
    except ValueError as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    all_tasks = tm.get_all()
    print("All tasks:", all_tasks)

    # Search for tasks
    try:
        search_results = tm.search("shopping")
        print("Search results for 'shopping':", search_results)

        search_results = tm.search("appointment")
        print("Search results for 'appointment':", search_results)

        search_results = tm.search("nonexistent")
        print("Search results for 'nonexistent':", search_results)
    except ValueError as e:
        print(f"Error searching: {e}")

    # Finish a task
    try:
        finished = tm.finish(id1)
        print(f"Task {id1} finished: {finished}")
        finished = tm.finish(999)  # Non-existent ID
        print(f"Task 999 finished: {finished}")
    except (TypeError, ValueError) as e:  # Catch both potential errors
        print(f"Error finishing task: {e}")


    # Get all tasks again (to see the finished task)
    all_tasks = tm.get_all()
    print("All tasks after finishing:", all_tasks)

    # Remove a task
    try:
        removed = tm.remove(id2)
        print(f"Task {id2} removed: {removed}")
        removed = tm.remove(999)  # Non-existent ID
        print(f"Task 999 removed: {removed}")
    except (TypeError, ValueError) as e:
        print(f"Error removing task: {e}")

    # Get all tasks again (after removal)
    all_tasks = tm.get_all()
    print("All tasks after removal:", all_tasks)

    # Clear all tasks
    cleared = tm.clear_all()
    print(f"All tasks cleared: {cleared}")

     # Get all tasks again (after clearing)
    all_tasks = tm.get_all()
    print("All tasks after clear all:", all_tasks)

    # Test adding an empty task name (should raise ValueError)
    try:
        tm.add("", "This should fail.")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # Test adding task with negative id (should raise ValueError)
    try:
        tm.remove(-1)
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # Test searching an empty  task (should raise ValueError)
    try:
        tm.search("")
    except ValueError as e:
        print(f"Caught expected error: {e}")
