class TaskManager:
    """
    Manages a to-do list with functionalities to add, remove, search,
    finish, retrieve, and clear tasks.  Implements an in-memory storage
    using a dictionary for efficient task management.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a counter for task IDs.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups by ID
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name: The name of the task (must not be empty).
            task_description: A description of the task.

        Returns:
            The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name is empty.
        """
        if not task_name:
            raise ValueError("Task name cannot be empty.")

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
        Removes a task from the to-do list by its ID.

        Args:
            task_id: The ID of the task to be removed.

        Returns:
            True if the task was successfully removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer
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
        Searches for tasks by name or description.

        Args:
            task_term: The search term (can be part of the name or description).

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if no tasks match or if the search term is empty.

        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term:
            raise ValueError("Search term cannot be empty.")

        results = []
        for task in self.tasks.values():
            if task_term.lower() in task["task_name"].lower() or task_term.lower() in task[
                "task_description"
            ].lower():
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to be marked as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise.

        Raises:
            TypeError: If task_id is not an integer
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
        Retrieves all tasks, both completed and incomplete.

        Returns:
            A list of dictionaries, where each dictionary represents a task.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks in the to-do list.

        Returns:
           Always returns True, indicating that the task list has been cleared.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset the ID counter
        return True


def main():
    """
    Main function to demonstrate the usage of TaskManager.
    """
    manager = TaskManager()

    try:
        # Add tasks
        task1_id = manager.add("Grocery Shopping", "Buy milk, eggs, bread, and cheese")
        task2_id = manager.add("Book Doctor Appointment", "Schedule a check-up")
        print(f"Added Task 1 ID: {task1_id}, Task 2 ID: {task2_id}")

        # Get all tasks
        all_tasks = manager.get_all()
        print("All Tasks:", all_tasks)

        # Search for tasks
        search_results = manager.search("doctor")
        print("Search Results for 'doctor':", search_results)

        search_results = manager.search("buy")
        print("Search Results for 'buy':", search_results)

        # Finish a task
        finished = manager.finish(task1_id)
        print(f"Finished Task 1: {finished}")

        # Get all tasks again
        all_tasks = manager.get_all()
        print("All Tasks (after finishing one):", all_tasks)

        # Remove a task
        removed = manager.remove(task2_id)
        print(f"Removed Task 2: {removed}")

        # Get all tasks after removal
        print("All Tasks (after removal):", manager.get_all())

        # Test error conditions
        try:
            manager.add("", "This should raise an error")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            manager.remove(-1)
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            manager.search("")
        except ValueError as e:
            print(f"Caught expected error: {e}")


        # Clear all
        manager.clear_all()
        print("All tasks after clearing:", manager.get_all())


    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

