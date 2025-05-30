class TaskManager:
    """
    A task manager for handling a console-based to-do list.
    
    This class implements functions to add, remove, search, finish, retrieve,
    and clear tasks. Each task is stored as a dictionary with keys:
    (id, task_name, task_description, is_finished).
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an in-memory data store.
        """
        self.tasks = {}  # Stores tasks keyed by unique ID.
        self.next_id = 1  # Unique task ID generator.

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID of the newly added task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_id
        self.tasks[task_id] = {
            'id': task_id,
            'task_name': task_name,
            'task_description': task_description,
            'is_finished': False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was removed; False if not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Searches for tasks by name or description containing the search term.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of task dictionaries matching the search term.

        Raises:
            ValueError: If the search term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = task_term.lower()
        matching_tasks = [
            task for task in self.tasks.values()
            if term_lower in task['task_name'].lower() or term_lower in task['task_description'].lower()
        ]
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The ID of the task to mark as completed.

        Returns:
            bool: True if the task was successfully marked as finished; False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]['is_finished'] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: A list of all tasks with their details.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            bool: True after clearing all tasks.
        """
        self.tasks.clear()
        return True


def print_task(task: dict) -> None:
    """
    Prints a single task in a user-friendly format.

    Args:
        task (dict): A task dictionary containing id, task_name, task_description, and is_finished.
    """
    print(
        f"ID: {task['id']} | "
        f"Name: {task['task_name']} | "
        f"Description: {task['task_description']} | "
        f"Finished: {task['is_finished']}"
    )


def main():
    """
    The main function driving the console-based to-do list application.
    Provides a menu interface to interact with the TaskManager.
    """
    manager = TaskManager()

    menu = (
        "\nPlease choose an option:\n"
        "1. Add task\n"
        "2. Remove task\n"
        "3. Search tasks\n"
        "4. Finish task\n"
        "5. Show all tasks\n"
        "6. Clear all tasks\n"
        "7. Exit\n"
        "Enter your choice (1-7): "
    )

    while True:
        try:
            choice = input(menu).strip()

            if choice == '1':
                # Add task
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = manager.add(task_name, task_description)
                print(f"Task added with ID: {task_id}")

            elif choice == '2':
                # Remove task
                task_id_input = input("Enter task ID to remove: ").strip()
                if not task_id_input.isdigit():
                    print("Invalid input. Please enter a positive integer for task ID.")
                    continue
                task_id = int(task_id_input)
                if manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")

            elif choice == '3':
                # Search tasks
                search_term = input("Enter search term: ").strip()
                results = manager.search(search_term)
                if results:
                    print("Matching tasks:")
                    for task in results:
                        print_task(task)
                else:
                    print("No tasks match the given search term.")

            elif choice == '4':
                # Finish task
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                if not task_id_input.isdigit():
                    print("Invalid input. Please enter a positive integer for task ID.")
                    continue
                task_id = int(task_id_input)
                if manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")

            elif choice == '5':
                # Show all tasks
                tasks = manager.get_all()
                if tasks:
                    print("All tasks:")
                    for task in tasks:
                        print_task(task)
                else:
                    print("No tasks available.")

            elif choice == '6':
                # Clear all tasks
                confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirm == "yes":
                    manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear all cancelled.")

            elif choice == '7':
                # Exit
                print("Exiting application.")
                break

            else:
                print("Invalid choice. Please select a valid option (1-7).")

        except ValueError as e:
            # Catch and display any validation errors.
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
