class TaskManager:
    """
    TaskManager manages todo tasks in memory.
    Each task is stored as a dictionary with the following keys:
    - id: unique task identifier (int)
    - task_name: name of the task (str)
    - task_description: description of the task (str)
    - is_finished: status flag indicating if the task is completed (bool)
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task storage and a counter for unique IDs.
        """
        self.tasks = {}      # Dictionary for quick lookup (id -> task dict)
        self.next_id = 1     # Auto-incrementing task ID

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task with the given name and description.

        Args:
            task_name (str): The name of the task. Must not be empty.
            task_description (str): The description of the task. Must not be empty.

        Raises:
            ValueError: If task_name or task_description is empty or contains only whitespace.

        Returns:
            int: The unique identifier (ID) assigned to the new task.
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
            "is_finished": False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id (int): The ID of the task to remove. Must be a positive integer.

        Raises:
            ValueError: If task_id is not a positive integer.

        Returns:
            bool: True if the task existed and was removed; False if the task was not found.
        """
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Searches tasks by name or description.

        Args:
            task_term (str): The term to search for. Must not be empty.

        Raises:
            ValueError: If task_term is empty or only whitespace.

        Returns:
            list[dict]: A list of tasks (as dictionaries) that match the search criteria.
                        Each task is in the format:
                        {"id": id, "task_name": name, "task_description": description, "is_finished": finished_flag}
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = task_term.lower()
        matching_tasks = [
            task for task in self.tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to mark as finished. Must be a positive integer.

        Raises:
            ValueError: If task_id is not a positive integer.

        Returns:
            bool: True if the task was found and marked as finished; False otherwise.
        """
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all the tasks.

        Returns:
            list[dict]: A list of all task dictionaries.
                        Each task is formatted as: (id, task_name, task_description, is_finished)
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Clears all tasks from the task manager.

        Returns:
            bool: True upon successful clearance.
        """
        self.tasks.clear()
        return True


def print_task(task: dict) -> None:
    """
    Prints a single task's details in the format:
    (id, task_name, task_description, is_finished)

    Args:
        task (dict): The task dictionary.
    """
    print(f"({task['id']}, {task['task_name']}, {task['task_description']}, {task['is_finished']})")


def display_all_tasks(task_manager: TaskManager) -> None:
    """
    Prints all tasks stored in the TaskManager.
    
    Args:
        task_manager (TaskManager): The instance of TaskManager.
    """
    tasks = task_manager.get_all()
    if not tasks:
        print("No tasks found.")
    else:
        print("\nAll Tasks:")
        for task in tasks:
            print_task(task)
        print()  # For spacing


def display_search_results(tasks: list) -> None:
    """
    Prints the search results.

    Args:
        tasks (list): List of task dictionaries that match a search query.
    """
    if not tasks:
        print("No matching tasks found.")
    else:
        print("\nMatching Tasks:")
        for task in tasks:
            print_task(task)
        print()


def main():
    """
    Runs the console-based todo list app with a menu-driven interface.
    The app supports adding, removing, searching, finishing, displaying, and clearing tasks.
    """
    task_manager = TaskManager()

    menu = """
---- Todo List Application ----
Select an option:
1. Add a task
2. Remove a task
3. Search tasks
4. Mark task as finished
5. Display all tasks
6. Clear all tasks
7. Exit
"""

    while True:
        print(menu)
        option = input("Enter your choice (1-7): ").strip()

        if option == "1":
            # Add a task
            try:
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID {task_id}.")
            except ValueError as error:
                print(f"Error: {error}")

        elif option == "2":
            # Remove a task
            try:
                task_id_str = input("Enter task ID to remove: ").strip()
                if not task_id_str.isdigit():
                    print("Invalid input: Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_str)
                if task_manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"Task with ID {task_id} does not exist.")
            except ValueError as error:
                print(f"Error: {error}")

        elif option == "3":
            # Search tasks
            try:
                term = input("Enter search term: ").strip()
                results = task_manager.search(term)
                display_search_results(results)
            except ValueError as error:
                print(f"Error: {error}")

        elif option == "4":
            # Mark task as finished
            try:
                task_id_str = input("Enter task ID to mark as finished: ").strip()
                if not task_id_str.isdigit():
                    print("Invalid input: Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_str)
                if task_manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
                else:
                    print(f"Task with ID {task_id} does not exist.")
            except ValueError as error:
                print(f"Error: {error}")

        elif option == "5":
            # Display all tasks
            display_all_tasks(task_manager)

        elif option == "6":
            # Clear all tasks
            confirmation = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
            if confirmation == 'y':
                task_manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Clear operation canceled.")

        elif option == "7":
            print("Exiting application. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option (1-7).")

        input("Press Enter to continue...")


if __name__ == "__main__":
    main()
