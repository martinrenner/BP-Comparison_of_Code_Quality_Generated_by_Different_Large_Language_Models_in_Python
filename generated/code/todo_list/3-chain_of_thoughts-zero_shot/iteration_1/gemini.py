class TaskManager:
    """
    Manages a list of tasks, allowing adding, removing, searching,
    finishing, retrieving, and clearing tasks.  Implements an in-memory
    todo list adhering to best practices and ISO/IEC 25010 quality
    characteristics.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and sets the
        initial task ID to 1.
        """
        self.tasks = {}  # Dictionary to store tasks: {id: task_data}
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the todo list.

        Args:
            task_name: The name of the task (must not be empty).
            task_description: The description of the task (must not be empty).

        Returns:
            The unique ID of the newly added task.

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
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the todo list by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.

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
        Searches for tasks matching a given term in either the name or description.

        Args:
            task_term: The search term (can be empty).

        Returns:
            A list of dictionaries, each representing a matching task
            (empty list if no matches are found).  Each dictionary
            includes 'id', 'task_name', 'task_description', and 'is_finished'.

        Raises:
             TypeError: if task_term is not a string
        """
        if not isinstance(task_term, str):
            raise TypeError("The search term must be a string type")

        results = []
        for task in self.tasks.values():
            if task_term.lower() in task["task_name"].lower() or task_term.lower() in task["task_description"].lower():
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished by its ID.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished,
            False otherwise (e.g., task ID not found).

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
        Retrieves all tasks in the todo list.

        Returns:
             A list of dictionaries.  Empty list if there is no tasks
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Clears all tasks from the todo list.

        Returns:
            True (always returns True, as clearing is always successful).
        """
        self.tasks.clear()
        return True



# Example usage and testing
if __name__ == "__main__":
    tm = TaskManager()

    # Add tasks
    try:
        id1 = tm.add("Grocery Shopping", "Buy milk, eggs, and bread")
        id2 = tm.add("Book Doctor Appointment", "Routine checkup")
        print(f"Added tasks with IDs: {id1}, {id2}")
    except ValueError as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    all_tasks = tm.get_all()
    print("All tasks:", all_tasks)

    # Search for tasks
    search_results = tm.search("appointment")
    print("Search results:", search_results)
    search_results = tm.search("nonexistent")
    print("Search results (empty):", search_results)

    # Finish a task
    try:
        finished = tm.finish(id1)
        print(f"Finished task {id1}: {finished}")
        finished = tm.finish(999)  # Non-existent ID
        print(f"Finished task 999: {finished}")
    except (TypeError, ValueError) as e:
        print(f"Error finishing task: {e}")

    # Get all tasks again (to see the finished task)
    all_tasks = tm.get_all()
    print("All tasks (after finishing):", all_tasks)

    # Remove a task
    try:
        removed = tm.remove(id2)
        print(f"Removed task {id2}: {removed}")
        removed = tm.remove(999)  # Non-existent ID
        print(f"Removed task 999: {removed}")
    except (TypeError, ValueError) as e:
        print(f"Error removing task: {e}")

    # Get all tasks again (to see the removed task)
    all_tasks = tm.get_all()
    print("All tasks (after removing):", all_tasks)

    # Clear all tasks
    cleared = tm.clear_all()
    print(f"Cleared all tasks: {cleared}")

    # Get all tasks (should be empty)
    all_tasks = tm.get_all()
    print("All tasks (after clearing):", all_tasks)

    # Example of adding an empty task name, raising a ValueError
    try:
        tm.add("", "This should raise an error")
    except ValueError as e:
        print(f"Caught expected error: {e}")

     # Example of adding an empty task description, raising a ValueError
    try:
        tm.add("Task with empty description", "")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # Example of removing invalid id, raising an ValueError
    try:
        tm.remove(-15)
    except ValueError as e:
        print(f"Caught expected error: {e}")

      # Example of removing invalid id type, raising an TypeError
    try:
        tm.remove("123")
    except TypeError as e:
        print(f"Caught expected error: {e}")

      # Example of finishing invalid id, raising an ValueError
    try:
        tm.finish(-1)
    except ValueError as e:
        print(f"Caught expected error: {e}")

      # Example of finishing invalid id type, raising an TypeError
    try:
        tm.finish("123")
    except TypeError as e:
        print(f"Caught expected error: {e}")

    # Example of searching invalid type, raising an TypeError
    try:
        tm.search(123)
    except TypeError as e:
        print(f"Caught expected error: {e}")

