class TaskManager:
    """
    Class to manage tasks in a console-based to-do list application.
    Each task is represented as a dictionary with the format:
    {
        "id": int,
        "task_name": str,
        "task_description": str,
        "is_finished": bool
    }
    """

    def __init__(self):
        # Store tasks in a dictionary for efficient lookups, insertions, and deletions.
        # Keys are task IDs, values are dictionaries containing task details.
        self.tasks = {}
        # A counter to generate unique task IDs.
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task.

        :param task_name: The name of the task (must be non-empty).
        :param task_description: The description of the task (must be non-empty).
        :return: The unique ID assigned to the task.
        :raises ValueError: If the task name or description is empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        :param task_id: The unique ID of the task to remove.
        :return: True if the task was found and removed; False otherwise.
        :raises ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks whose name or description includes the search term.

        :param task_term: The term to search for (must be non-empty).
        :return: A list of matching tasks as dictionaries.
        :raises ValueError: If the search term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term_lower = task_term.strip().lower()
        results = [
            task.copy() for task in self.tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        :param task_id: The ID of the task to mark as finished.
        :return: True if the task is found and marked as finished; False otherwise.
        :raises ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks.

        :return: A list of all tasks with complete details.
        """
        return [task.copy() for task in self.tasks.values()]

    def clear_all(self) -> bool:
        """
        Clears all tasks.

        :return: True after all tasks have been successfully cleared.
        """
        self.tasks.clear()
        return True


def main():
    """
    Entry point for the console-based to-do list application.
    Provides a simple menu for interacting with the TaskManager.
    """
    task_manager = TaskManager()

    menu = (
        "\nTo-Do List Application\n"
        "------------------------------\n"
        "1. Add Task\n"
        "2. Remove Task\n"
        "3. Search Tasks\n"
        "4. Finish Task\n"
        "5. Get All Tasks\n"
        "6. Clear All Tasks\n"
        "7. Exit\n"
        "------------------------------\n"
    )

    while True:
        print(menu)
        choice = input("Select an option (1-7): ").strip()

        if choice == "1":  # Add Task
            try:
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "2":  # Remove Task
            try:
                task_id_input = input("Enter the task ID to remove: ").strip()
                if not task_id_input.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(task_id_input)
                if task_manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "3":  # Search Tasks
            try:
                term = input("Enter search term: ").strip()
                matching_tasks = task_manager.search(term)
                if matching_tasks:
                    print("Matching Tasks:")
                    for task in matching_tasks:
                        print(
                            f"ID: {task['id']}, "
                            f"Name: {task['task_name']}, "
                            f"Description: {task['task_description']}, "
                            f"Finished: {task['is_finished']}"
                        )
                else:
                    print("No matching tasks found.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "4":  # Finish Task
            try:
                task_id_input = input("Enter the task ID to mark as finished: ").strip()
                if not task_id_input.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(task_id_input)
                if task_manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "5":  # Get All Tasks
            tasks = task_manager.get_all()
            if tasks:
                print("All Tasks:")
                for task in tasks:
                    print(
                        f"ID: {task['id']}, "
                        f"Name: {task['task_name']}, "
                        f"Description: {task['task_description']}, "
                        f"Finished: {task['is_finished']}"
                    )
            else:
                print("No tasks available.")

        elif choice == "6":  # Clear All Tasks
            confirmation = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirmation == "yes":
                task_manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Clear all tasks cancelled.")

        elif choice == "7":  # Exit
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid option. Please select a valid number between 1 and 7.")


if __name__ == "__main__":
    main()
