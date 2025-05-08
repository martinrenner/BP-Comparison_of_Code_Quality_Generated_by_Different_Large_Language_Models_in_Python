"""
Console-based To-Do List Application

This application manages tasks with basic operations such as adding, removing,
searching, finishing, retrieving, and clearing tasks. The implementation follows
object-oriented design principles and common best practices for efficiency,
modularity, and maintainability.
"""

class TaskManager:
    """
    Manages tasks for the To-Do List application.
    
    Attributes:
        tasks (dict): A dictionary that stores task records with task_id as keys.
        _next_id (int): A counter that generates unique task IDs.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a next_id counter.
        """
        self.tasks = {}
        self._next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A brief description of the task.

        Returns:
            int: The unique ID assigned to the added task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not task_name.strip() or not task_description.strip():
            raise ValueError("Task name and description cannot be empty.")
        
        task_id = self._next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed; False if the task ID does not exist.

        Raises:
            ValueError: If task_id is negative.
        """
        if task_id < 0:
            raise ValueError("Task ID must be non-negative.")
        
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Searches for tasks whose name or description contains the given search term.

        Args:
            task_term (str): The term to search for in task names or descriptions.

        Returns:
            list: A list of tasks (dictionaries) that match the search criteria.

        Raises:
            ValueError: If the search term is an empty string.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")
        
        term_lower = task_term.lower()
        results = [
            task for task in self.tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The unique ID of the task to finish.

        Returns:
            bool: True if the task was found and marked as finished; False otherwise.

        Raises:
            ValueError: If task_id is negative.
        """
        if task_id < 0:
            raise ValueError("Task ID must be non-negative.")
        
        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all tasks in the to-do list.

        Returns:
            list: A list of all tasks, where each task is represented as a dictionary.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks in the to-do list.

        Returns:
            bool: True if all tasks were successfully cleared.
        """
        self.tasks.clear()
        self._next_id = 1  # Reset the task ID counter for a fresh start.
        return True


def display_menu():
    """
    Displays the list of available commands for the application.
    """
    print("\nAvailable commands:")
    print("  add       - Add a new task")
    print("  remove    - Remove a task by ID")
    print("  search    - Search for tasks")
    print("  finish    - Mark a task as finished")
    print("  get_all   - Get all tasks")
    print("  clear_all - Clear all tasks")
    print("  exit      - Exit the application\n")


def main():
    """
    Runs the console-based to-do list application, accepting user commands and
    executing the corresponding task manager operations.
    """
    task_manager = TaskManager()
    print("Welcome to the To-Do List Application!")
    display_menu()

    while True:
        command = input("Enter command: ").strip().lower()

        if command == "add":
            try:
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = task_manager.add(task_name, task_description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as e:
                print(f"Error: {e}")

        elif command == "remove":
            try:
                task_id_input = input("Enter task ID to remove: ").strip()
                if not task_id_input.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(task_id_input)
                if task_manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"No task found with ID {task_id}.")
            except ValueError as e:
                print(f"Error: {e}")

        elif command == "search":
            try:
                search_term = input("Enter search term: ").strip()
                matching_tasks = task_manager.search(search_term)
                if matching_tasks:
                    print("Matching tasks found:")
                    for task in matching_tasks:
                        print(task)
                else:
                    print("No matching tasks found.")
            except ValueError as e:
                print(f"Error: {e}")

        elif command == "finish":
            try:
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                if not task_id_input.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(task_id_input)
                if task_manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
                else:
                    print(f"No task found with ID {task_id}.")
            except ValueError as e:
                print(f"Error: {e}")

        elif command == "get_all":
            all_tasks = task_manager.get_all()
            if all_tasks:
                print("Current tasks:")
                for task in all_tasks:
                    print(task)
            else:
                print("No tasks available.")

        elif command == "clear_all":
            confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirm == "yes":
                task_manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Operation cancelled.")

        elif command == "exit":
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid command. Please try again.")
            display_menu()


if __name__ == '__main__':
    main()
