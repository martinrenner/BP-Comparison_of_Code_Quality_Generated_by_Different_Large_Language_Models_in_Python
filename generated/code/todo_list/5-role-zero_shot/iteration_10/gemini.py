class TaskManager:
    """
    Manages a to-do list with functionalities to add, remove, search,
    mark as finished, retrieve all, and clear all tasks.  The class
    adheres to high standards of software quality, including efficiency,
    maintainability, and robustness, in line with ISO/IEC 25010.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty list of tasks and
        sets the initial task ID to 0.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups by ID
        self.next_task_id = 0

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

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
        Removes a task from the to-do list by its ID.

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
            return False  # Task not found

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks that contain the given term in their name or description.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of tasks that match the search term.  Returns an
                        empty list if no matches are found or if the search term is empty.

        Raises:
            ValueError: if the task_term is empty
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty")

        results = []
        for task in self.tasks.values():
            if task_term.lower() in task["name"].lower() or task_term.lower() in task[
                "description"
            ].lower():
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

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
        Retrieves all tasks in the to-do list, including their details.

        Returns:
            list[dict]: A list of all tasks, where each task is a dictionary
                       containing 'id', 'name', 'description', and 'is_finished' keys.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the to-do list.

        Returns:
            bool: True after successfully clearing all tasks.  Always returns True,
                  even if the list was already empty.
        """
        self.tasks.clear()
        self.next_task_id = 0  # Reset the task ID counter
        return True


def main():
    """
    Main function to demonstrate the TaskManager class.
    """

    tm = TaskManager()

    try:
        # Add tasks
        task1_id = tm.add("Grocery Shopping", "Buy milk, eggs, and bread")
        task2_id = tm.add("Book Doctor Appt", "Schedule annual checkup")

        # Get all tasks
        print("All tasks:", tm.get_all())

        # Finish a task
        tm.finish(task1_id)
        print(f"Task {task1_id} finished.")
        print("All tasks after finishing:", tm.get_all())

        # Search for a task
        search_results = tm.search("Doctor")
        print("Search results for 'Doctor':", search_results)

        # Remove a task
        tm.remove(task2_id)
        print(f"Task {task2_id} removed.")
        print("All tasks after removal:", tm.get_all())

        # Add task with spaces
        task3_id = tm.add("  Laundry  ", "   Wash whites    ")
        print("All tasks after whitespace test:", tm.get_all())

        # Clear all tasks
        tm.clear_all()
        print("To-do list cleared.")
        print("All tasks after clearing:", tm.get_all())

    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

