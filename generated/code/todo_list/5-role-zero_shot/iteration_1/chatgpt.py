class TaskManager:
    """
    TaskManager manages a console-based to-do list.
    
    Each task is a dictionary containing:
        - id (int): Unique identifier for the task.
        - task_name (str): Name of the task.
        - task_description (str): Description of the task.
        - is_finished (bool): Status indicating if the task is completed.
    
    This class provides methods to add, remove, search, finish, retrieve all, and clear tasks.
    """

    def __init__(self):
        # In-memory storage for tasks: mapping task_id to task dictionary.
        self.tasks = {}
        # Next unique task ID.
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name (str): The name of the task. Must not be an empty string.
            task_description (str): The description of the task. Must not be an empty string.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is not provided.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise ValueError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

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
        Removes a task with the specified task_id.

        Args:
            task_id (int): The unique ID of the task to remove. Must be a positive integer.

        Returns:
            bool: True if the task was successfully removed, False if the task_id does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            return False  # Task not found.
        del self.tasks[task_id]
        return True

    def search(self, task_term: str) -> list:
        """
        Searches tasks whose name or description contains the search term (case-insensitive).

        Args:
            task_term (str): The search term. Must not be empty.

        Returns:
            list[dict]: A list of tasks matching the search term.

        Raises:
            ValueError: If the search term is not a string or is empty.
        """
        if not isinstance(task_term, str):
            raise ValueError("Search term must be a string.")
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
        Marks the task with the specified task_id as finished.

        Args:
            task_id (int): The unique ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            return False  # Task not found.
        self.tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> list:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: A list of all tasks, each represented as a dictionary in the format:
                        (id, task_name, task_description, is_finished)
        """
        # Return tasks sorted by their ID.
        return sorted(self.tasks.values(), key=lambda task: task["id"])

    def clear_all(self) -> bool:
        """
        Clears all tasks from the to-do list.

        Returns:
            bool: True if tasks were cleared.
        """
        self.tasks.clear()
        # Optionally reset the task ID counter.
        self.next_id = 1
        return True


def display_task(task: dict):
    """
    Utility function to display a task in the format:
    (id, task_name, task_description, is_finished)

    Args:
        task (dict): The task dictionary.
    """
    print(f"({task['id']}, {task['task_name']}, {task['task_description']}, {task['is_finished']})")


def main():
    """
    Entry point for the console-based to-do list application.
    
    Provides a menu for users to:
        - Add a task.
        - Remove a task.
        - Search for tasks.
        - Mark a task as finished.
        - List all tasks.
        - Clear all tasks.
        - Exit the application.
    """
    tm = TaskManager()
    
    menu = """
-----------------------------
Please select an option:
1. Add Task
2. Remove Task
3. Search Tasks
4. Finish Task
5. List All Tasks
6. Clear All Tasks
7. Exit
-----------------------------
"""
    while True:
        print(menu)
        choice = input("Enter your choice (1-7): ").strip()
        if choice == "1":
            try:
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = tm.add(name, description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "2":
            try:
                task_id_input = input("Enter task ID to remove: ").strip()
                task_id = int(task_id_input)
                if tm.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "3":
            try:
                search_term = input("Enter search term: ").strip()
                results = tm.search(search_term)
                if results:
                    print("Matching Tasks:")
                    for task in results:
                        display_task(task)
                else:
                    print("No tasks found matching the search criteria.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "4":
            try:
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                task_id = int(task_id_input)
                if tm.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "5":
            tasks = tm.get_all()
            if tasks:
                print("All Tasks:")
                for task in tasks:
                    display_task(task)
            else:
                print("No tasks available.")

        elif choice == "6":
            confirm = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
            if confirm == "y":
                tm.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Clear operation canceled.")

        elif choice == "7":
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid option. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
