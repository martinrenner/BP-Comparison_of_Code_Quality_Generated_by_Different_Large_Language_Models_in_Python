class TaskManager:
    """
    TaskManager class for managing tasks in a todo list application.
    Each task is represented as a dictionary with the structure:
      {
         "id": int,
         "task_name": str,
         "task_description": str,
         "is_finished": bool
      }
    The class provides methods to add, remove, search, finish tasks,
    retrieve all tasks, and clear all tasks.
    """

    def __init__(self):
        """
        Initialize the TaskManager with an empty dictionary for task storage
        and a counter to generate unique task IDs.
        """
        self.tasks = {}  # Key: task ID, Value: task dictionary
        self.next_id = 1  # Counter for unique task IDs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the todo list.

        Args:
            task_name (str): The name of the task. Must not be an empty string.
            task_description (str): The description of the task. Must not be empty.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If the task name or description is empty.
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
        self.next_id += 1  # Update the ID counter for the next task
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the todo list by its ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False if the task does not exist.

        Raises:
            ValueError: If task_id is negative or not an integer.
        """
        if not isinstance(task_id, int) or task_id < 0:
            raise ValueError("Task ID must be a non-negative integer.")
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Searches for tasks that have the search term in the task name or description.

        Args:
            task_term (str): The search term to look for. Must not be an empty string.

        Returns:
            list: A list of task dictionaries that match the search term.

        Raises:
            ValueError: If the search term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        search_results = []
        term_lower = task_term.lower()
        for task in self.tasks.values():
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower():
                search_results.append(task)
        return search_results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished based on its ID.

        Args:
            task_id (int): The unique ID of the task.

        Returns:
            bool: True if the task was found and marked as finished, False if not.

        Raises:
            ValueError: If task_id is negative or not an integer.
        """
        if not isinstance(task_id, int) or task_id < 0:
            raise ValueError("Task ID must be a non-negative integer.")
        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Gets all tasks stored in the todo list in a consistent sorted order.

        Returns:
            list: A list of all task dictionaries.
        """
        # Return tasks sorted by their ID for consistent ordering.
        return [self.tasks[task_id] for task_id in sorted(self.tasks)]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the todo list.

        Returns:
            bool: True after all tasks are deleted.
        """
        self.tasks.clear()
        return True


def print_task(task: dict):
    """
    Prints details of a single task in a formatted manner.

    Args:
        task (dict): The task dictionary to print.
    """
    status = "Finished" if task["is_finished"] else "Pending"
    print(f'ID: {task["id"]}, Name: {task["task_name"]}, '
          f'Description: {task["task_description"]}, Status: {status}')


def print_all_tasks(tasks: list):
    """
    Prints all tasks from a list.

    Args:
        tasks (list): A list of task dictionaries.
    """
    if not tasks:
        print("No tasks to display.")
    else:
        for task in tasks:
            print_task(task)


def print_help():
    """
    Displays available commands and their usage.
    """
    print("""
Available commands:
    add         - Add a new task. Usage: add <task_name> <task_description>
    remove      - Remove a task by ID. Usage: remove <task_id>
    search      - Search tasks by term. Usage: search <search_term>
    finish      - Mark a task as finished. Usage: finish <task_id>
    get_all     - Display all tasks. Usage: get_all
    clear_all   - Delete all tasks. Usage: clear_all
    help        - Show this help message.
    exit        - Exit the application.
""")


def main():
    """
    Main function to run the console-based todo list app.
    Runs an interactive command loop where the user can perform
    add, remove, search, finish, get_all, and clear_all operations.
    """
    manager = TaskManager()

    print("Welcome to the Console-based Todo List App!")
    print_help()

    while True:
        try:
            user_input = input("\nEnter command: ").strip()
            if not user_input:
                continue

            # Tokenize the input based on spaces
            tokens = user_input.split()
            command = tokens[0].lower()

            if command == "exit":
                print("Exiting the application. Goodbye!")
                break

            elif command == "help":
                print_help()

            elif command == "add":
                if len(tokens) < 3:
                    print("Usage: add <task_name> <task_description>")
                    continue
                # Using first token as task name and the rest as task description
                task_name = tokens[1]
                task_description = " ".join(tokens[2:])
                task_id = manager.add(task_name, task_description)
                print(f"Task added with ID: {task_id}")

            elif command == "remove":
                if len(tokens) != 2:
                    print("Usage: remove <task_id>")
                    continue
                try:
                    task_id = int(tokens[1])
                except ValueError:
                    print("Invalid input: Task ID must be an integer.")
                    continue

                if manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"Task with ID {task_id} not found.")

            elif command == "search":
                if len(tokens) < 2:
                    print("Usage: search <search_term>")
                    continue
                search_term = " ".join(tokens[1:])
                results = manager.search(search_term)
                if not results:
                    print("No matching tasks found.")
                else:
                    print(f"Found {len(results)} task(s):")
                    print_all_tasks(results)

            elif command == "finish":
                if len(tokens) != 2:
                    print("Usage: finish <task_id>")
                    continue
                try:
                    task_id = int(tokens[1])
                except ValueError:
                    print("Invalid input: Task ID must be an integer.")
                    continue

                if manager.finish(task_id):
                    print(f"Task with ID {task_id} has been marked as finished.")
                else:
                    print(f"Task with ID {task_id} not found.")

            elif command == "get_all":
                tasks = manager.get_all()
                print_all_tasks(tasks)

            elif command == "clear_all":
                confirmation = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirmation == "yes":
                    manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear operation cancelled.")

            else:
                print("Unknown command. Type 'help' to see available commands.")

        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")


if __name__ == "__main__":
    main()
