class TaskManager:
    """
    A task manager for handling a console-based to-do list application.
    
    This class supports adding, removing, searching, marking tasks as finished,
    retrieving all tasks, and clearing all tasks. Each task is represented as a
    dictionary with the following keys: 'id', 'task_name', 'task_description', 'is_finished'.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty task store and an ID counter.
        """
        self._tasks: dict[int, dict] = {}
        self._id_counter: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID of the newly added task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")
        
        task_id = self._id_counter
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self._id_counter += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task with the given ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.

        Raises:
            ValueError: If task_id is negative.
        """
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks by matching the search term in the task's name
        or description. The search is case-insensitive.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of tasks (as dictionaries) that match the search term.

        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = task_term.lower()
        matches = [
            task for task in self._tasks.values()
            if lower_term in task["task_name"].lower() or lower_term in task["task_description"].lower()
        ]
        return matches

    def finish(self, task_id: int) -> bool:
        """
        Marks the task with the given ID as finished.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was successfully marked as finished, False otherwise.

        Raises:
            ValueError: If task_id is negative.
        """
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")

        if task_id in self._tasks:
            self._tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the manager.

        Returns:
            list[dict]: A list of all tasks with their details.
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Clears all tasks from the manager.

        Returns:
            bool: True if all tasks were successfully cleared.
        """
        self._tasks.clear()
        return True


def display_menu() -> None:
    """
    Displays the available commands to the user.
    """
    menu = (
        "\n--- To-Do List Application ---\n"
        "1. Add a task\n"
        "2. Remove a task\n"
        "3. Search tasks\n"
        "4. Mark a task as finished\n"
        "5. List all tasks\n"
        "6. Clear all tasks\n"
        "7. Exit\n"
    )
    print(menu)


def main() -> None:
    """
    The main function that runs the console-based to-do list application.
    It handles user interactions and calls the TaskManager methods accordingly.
    """
    manager = TaskManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            # Add a task
            try:
                task_name = input("Enter the task name: ").strip()
                task_description = input("Enter the task description: ").strip()
                task_id = manager.add(task_name, task_description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            # Remove a task
            try:
                task_id_input = input("Enter the task ID to remove: ").strip()
                task_id = int(task_id_input)
                if manager.remove(task_id):
                    print(f"Task {task_id} removed successfully.")
                else:
                    print(f"Task {task_id} does not exist.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            # Search tasks
            try:
                term = input("Enter the search term: ").strip()
                matches = manager.search(term)
                if matches:
                    print("Matching tasks:")
                    for task in matches:
                        print(task)
                else:
                    print("No matching tasks found.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            # Mark a task as finished
            try:
                task_id_input = input("Enter the task ID to mark as finished: ").strip()
                task_id = int(task_id_input)
                if manager.finish(task_id):
                    print(f"Task {task_id} marked as finished.")
                else:
                    print(f"Task {task_id} does not exist.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            # List all tasks
            tasks = manager.get_all()
            if tasks:
                print("All tasks:")
                for task in tasks:
                    print(task)
            else:
                print("No tasks found.")

        elif choice == "6":
            # Clear all tasks
            confirm = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
            if confirm == "y":
                manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Clear all tasks operation cancelled.")

        elif choice == "7":
            # Exit the application
            print("Exiting the To-Do List Application.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == '__main__':
    main()
