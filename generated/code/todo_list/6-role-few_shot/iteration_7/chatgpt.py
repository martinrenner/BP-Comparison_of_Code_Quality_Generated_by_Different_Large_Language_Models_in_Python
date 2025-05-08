class TaskManager:
    """
    Manages a list of tasks with functionality to add, remove, search, finish tasks,
    retrieve all tasks, and clear the task list.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty tasks store and a counter for unique IDs.
        """
        self._tasks: dict[int, dict] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task with the provided name and description.

        Args:
            task_name (str): The name of the task. Must not be empty.
            task_description (str): A description of the task. Must not be empty.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task identified by its unique ID.

        Args:
            task_id (int): The unique ID of the task to remove. Must be positive.

        Returns:
            bool: True if the task was successfully removed, False if no such task exists.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True

        return False

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks that contain the search term in their name or description.

        Args:
            task_term (str): The keyword or phrase to search for. Must not be empty.

        Returns:
            list[dict]: A list of tasks that match the search criteria.

        Raises:
            ValueError: If the search term is an empty string.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = task_term.lower()
        matching_tasks = [
            task for task in self._tasks.values()
            if lower_term in task["task_name"].lower() or lower_term in task["task_description"].lower()
        ]
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks the task identified by task_id as completed.

        Args:
            task_id (int): The unique ID of the task to mark as finished. Must be positive.

        Returns:
            bool: True if the task was marked as finished, False if the task does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            self._tasks[task_id]["is_finished"] = True
            return True

        return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks with their details.

        Returns:
            list[dict]: A list containing all tasks in the format (id, task_name, task_description, is_finished).
        """
        # Optionally, we can return tasks sorted by their IDs for consistency.
        return [self._tasks[task_id] for task_id in sorted(self._tasks)]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the manager.

        Returns:
            bool: True after all tasks have been cleared.
        """
        self._tasks.clear()
        return True


def main() -> None:
    """
    Console-based interface to interact with the TaskManager.
    """
    task_manager = TaskManager()

    menu = """
--- To-Do List Application ---
Please choose an option:
1. Add Task
2. Remove Task
3. Search Tasks
4. Finish Task
5. Display All Tasks
6. Clear All Tasks
7. Exit
"""

    while True:
        print(menu)
        choice = input("Enter your choice (1-7): ").strip()

        try:
            if choice == "1":
                # Add a task
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")

            elif choice == "2":
                # Remove a task
                task_id_input = input("Enter task ID to remove: ").strip()
                try:
                    task_id = int(task_id_input)
                except ValueError:
                    print("Invalid task ID. Please enter a positive integer.")
                    continue

                if task_manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"No task found with ID {task_id}.")

            elif choice == "3":
                # Search tasks
                term = input("Enter search term: ").strip()
                results = task_manager.search(term)
                if results:
                    print("Matching tasks:")
                    for task in results:
                        finished_status = "Finished" if task["is_finished"] else "Pending"
                        print(f"ID: {task['id']}, Name: {task['task_name']}, Description: {task['task_description']}, Status: {finished_status}")
                else:
                    print("No matching tasks found.")

            elif choice == "4":
                # Mark a task as finished
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                try:
                    task_id = int(task_id_input)
                except ValueError:
                    print("Invalid task ID. Please enter a positive integer.")
                    continue

                if task_manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
                else:
                    print(f"No task found with ID {task_id}.")

            elif choice == "5":
                # Get all tasks
                tasks = task_manager.get_all()
                if tasks:
                    print("All tasks:")
                    for task in tasks:
                        finished_status = "Finished" if task["is_finished"] else "Pending"
                        print(f"ID: {task['id']}, Name: {task['task_name']}, Description: {task['task_description']}, Status: {finished_status}")
                else:
                    print("No tasks to display.")

            elif choice == "6":
                # Clear all tasks
                confirmation = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirmation in ("yes", "y"):
                    task_manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear operation cancelled.")

            elif choice == "7":
                # Exit the application
                print("Exiting the To-Do List Application. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

        except ValueError as e:
            print(f"Input error: {e}")
        except Exception as e:
            # General exception catcher for unforeseen errors.
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
