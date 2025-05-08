class TaskManager:
    """
    Manages a to-do list with functionalities to add, remove, search,
    finish, retrieve, and clear tasks.  Adheres to ISO/IEC 25010
    standards for maintainability, reliability, and efficiency.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a unique ID counter.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups (task_id: task_details)
        self.next_id = 1  # Keeps track of the next available task ID

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name: The name of the task (must not be empty).
            task_description: A description of the task.

        Returns:
            The unique ID assigned to the newly added task.

        Raises:
            ValueError: If task_name is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

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
            task_id: The ID of the task to be removed.

        Returns:
            True if the task was successfully removed, False otherwise.

        Raises:
            TypeError:  If task_id is not an integer
            ValueError: If task_id is not positive
        """

        if not type(task_id) is int:
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
            task_term: The search term (can be a partial or full match).

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if no tasks match.

        Raises:
            ValueError: if task_term is empty
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty")

        results = []
        for task in self.tasks.values():
            if (
                task_term.lower() in task["name"].lower()
                or task_term.lower() in task["description"].lower()
            ):
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to be marked as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.

        Raises:
            TypeError:  If task_id is not an integer
            ValueError: If task_id is not positive
        """
        if not type(task_id) is int:
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
            A list of dictionaries, where each dictionary represents a task.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the to-do list.

        Returns:
            Always returns True, indicating success.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset the ID counter
        return True


def main():
    """
    Main function to demonstrate the TaskManager class interactions.
    """

    manager = TaskManager()

    # Add tasks
    try:
        task1_id = manager.add("Grocery Shopping", "Buy milk, eggs, bread, and cheese.")
        task2_id = manager.add("Book Appointment", "Schedule a doctor's appointment.")
        print(f"Added Task 1 ID: {task1_id}")  # Output: 1
        print(f"Added Task 2 ID: {task2_id}")  # Output: 2
    except ValueError as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    all_tasks = manager.get_all()
    print(f"All Tasks (before finishing): {all_tasks}")

    # Finish a task
    try:
        finish_status = manager.finish(task1_id)  # Finish task 1
        print(f"Finish Task 1: {finish_status}")  # Output: True
        finish_status = manager.finish(999)  # Try to finish non-existent task
        print(f"Finish Task 999: {finish_status}")  # Output: False
    except (TypeError, ValueError) as e:
         print(f"Erro finish task: {e}")


    # Get all tasks (after finishing)
    all_tasks = manager.get_all()
    print(f"All Tasks (after finishing): {all_tasks}")

    # Search for a task
    try:
        search_results = manager.search("grocery")
        print(f"Search Results for 'grocery': {search_results}")
        search_results = manager.search("appointment")
        print(f"Search Results for 'appointment': {search_results}")
        search_results = manager.search("nonexistent")
        print(f"Search Results for 'nonexistent': {search_results}") # Output: empty list
    except ValueError as e:
        print(f"Error searching task: {e}")

    # Remove a task
    try:
        remove_status = manager.remove(task2_id)  # Remove task 2
        print(f"Remove Task 2: {remove_status}")  # Output: True
        remove_status = manager.remove(999)        #Try to remove non-existent task
        print(f"Remove Task 999: {remove_status}") # Output: False
    except (TypeError, ValueError) as e:
         print(f"Error removing task: {e}")    

    # Get all tasks (after removing)
    all_tasks = manager.get_all()
    print(f"All Tasks (after removing): {all_tasks}")

    # Clear all tasks
    clear_status = manager.clear_all()  # Clear
    print(f"Clear All Tasks : {clear_status}")  # Output: True

     # Get all tasks (after clear)
    all_tasks = manager.get_all()
    print(f"All Tasks (after clear): {all_tasks}") # Output: empty list


if __name__ == "__main__":
    main()

