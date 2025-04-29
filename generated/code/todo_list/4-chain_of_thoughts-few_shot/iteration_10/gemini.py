class Task:
    """
    Represents a single task in the todo list.
    """
    def __init__(self, task_id: int, task_name: str, task_description: str, is_finished: bool = False):
        """
        Initializes a new Task object.

        Args:
            task_id (int): Unique identifier for the task.
            task_name (str): Name of the task.
            task_description (str): Description of the task.
            is_finished (bool): Status of the task (completed or not). Defaults to False.

        Raises:
            TypeError: If task_id is not an integer, or if task_name/description are not strings.
            ValueError: If task_id is negative, or if task_name is empty.
        """
        if not isinstance(task_id, int):
            raise TypeError("task_id must be an integer.")
        if task_id < 0:
            raise ValueError("task_id must be non-negative.")
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("task_name and task_description must be strings.")
        if not task_name:
            raise ValueError("task_name cannot be empty.")
        if not isinstance(is_finished, bool):
            raise TypeError("is_finished must be a boolean value")

        self.id = task_id
        self.name = task_name
        self.description = task_description
        self.is_finished = is_finished

    def __str__(self):
        """
        Returns a string representation of the task.
        """
        status = "Finished" if self.is_finished else "Not Finished"
        return f"ID: {self.id}, Name: {self.name}, Description: {self.description}, Status: {status}"

    def to_dict(self):
        """
        Returns a dictionary representation of the task.
        """
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished,
        }



class TaskManager:
    """
    Manages a list of tasks.  Implements the core functionality of a todo list.
    """

    def __init__(self):
        """
        Initializes a new TaskManager object.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups by ID
        self.next_id = 1  # Keep track of the next available ID

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID of the newly added task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is an empty string.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name:
            raise ValueError("Task name cannot be empty.")

        new_task = Task(self.next_id, task_name, task_description)
        self.tasks[self.next_id] = new_task
        self.next_id += 1
        return new_task.id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the list by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
        """
        if not isinstance(task_id, int):
            raise TypeError("task_id must be an integer.")
        if task_id < 0:
            raise ValueError("task_id must be non-negative.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        else:
            return False  # Task not found

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks by name or description.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of dictionaries, each representing a matching task.

        Raises:
            TypeError: If task_term is not a string.
        """

        if not isinstance(task_term, str):
            raise TypeError("task_term must be a string.")

        results = []
        for task in self.tasks.values():
            if task_term.lower() in task.name.lower() or task_term.lower() in task.description.lower():
                results.append(task.to_dict())
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if task exists and marked as finished, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
        """

        if not isinstance(task_id, int):
            raise TypeError("task_id must be an integer.")
        if task_id < 0:
            raise ValueError("task_id must be non-negative.")

        task = self.tasks.get(task_id)
        if task:
            task.is_finished = True
            return True
        else:
            return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: A list of dictionaries, each representing a task.
        """
        return [task.to_dict() for task in self.tasks.values()]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the list.

        Returns:
            bool: Always returns True, indicating successful clearing.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset the ID counter
        return True

# --- Example Usage ---
if __name__ == "__main__":
    manager = TaskManager()

    # Add tasks
    try:
        id1 = manager.add("Grocery Shopping", "Buy milk, eggs, and bread")
        id2 = manager.add("Book Appointment", "Doctor's appointment at 2 PM")
        print(f"Added task with ID: {id1}")
        print(f"Added task with ID: {id2}")
    except (TypeError, ValueError) as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    all_tasks = manager.get_all()
    print("\nAll tasks:")
    for task in all_tasks:
        print(task)

    # Search for tasks
    search_results = manager.search("Buy")
    print("\nSearch results for 'Buy':")
    for task in search_results:
        print(task)

    # Finish a task
    try:
        if manager.finish(id1):
            print(f"\nTask with ID {id1} marked as finished.")
        else:
            print(f"\nTask with ID {id1} not found.")
    except (TypeError, ValueError) as e:
        print(f"Error finishing task: {e}")

       # Get all tasks after one finished
    all_tasks = manager.get_all()
    print("\nAll tasks (after finishing):")
    for task in all_tasks:
        print(task)

    # Remove a task
    try:
        if manager.remove(id2):
            print(f"\nTask with ID {id2} removed.")
        else:
            print(f"\nTask with ID {id2} not found.")
    except (TypeError, ValueError) as e:
        print(f"Error removing task: {e}")
    
        # Get all tasks after one removed
    all_tasks = manager.get_all()
    print("\nAll tasks (after removing):")
    for task in all_tasks:
        print(task)

    # Try to remove a non-existent task
    try:
        if manager.remove(999):
            print("\nTask with ID 999 removed (should not happen).")
        else:
            print("\nTask with ID 999 not found (expected).")
    except (TypeError, ValueError) as e:
        print(f"Error removing task: {e}")

    #Clear all
    manager.clear_all()
    print("\nTasks after clear_all():")
    print(manager.get_all())

    # Add task with an empty description (should be added)
    try:
        manager.add("Task with empty description", "")
        print("\nAdded task with empty description.")
    except Exception as e:
        print(f"\nFailed to add task with empty description: {e}")

    #Add and Get tasks with empty description
    all_tasks = manager.get_all()
    print("\nAll tasks:")
    for task in all_tasks:
        print(task)

    # Try to add a task with an empty name (Error expected)
    try:
        manager.add("", "This should fail")
    except ValueError as e:
        print(f"\nCaught expected error: {e}")

    # Try to add a task with a not string name (Error expected)
    try:
        manager.add(123, "This should fail")
    except TypeError as e:
        print(f"\nCaught expected error: {e}")

    # Try to finish a task with a negative ID (Error expected)
    try:
        manager.finish(-1)
    except ValueError as e:
        print(f"\nCaught expected error: {e}")
