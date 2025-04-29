class TaskManager:
    """
    TaskManager is a console-based todo list manager that supports adding, removing, searching,
    finishing tasks, retrieving all tasks, and clearing all tasks. All tasks are stored in an
    in-memory data structure for fast lookups, insertions, and deletions.

    Each task is represented as a dictionary with the following keys:
      - "id": Unique identifier of the task.
      - "task_name": Name of the task.
      - "task_description": Description of the task.
      - "is_finished": Boolean flag indicating task completion.
    """

    def __init__(self):
        """
        Initialize a new TaskManager instance.
        """
        self._tasks = {}  # Dictionary to store tasks with unique IDs as keys
        self._next_id = 1  # Next unique ID to assign

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a task with the given name and description.
        
        Args:
            task_name (str): The name/title of the task.
            task_description (str): The detailed description of the task.
        
        Returns:
            int: The unique task ID assigned.
        
        Raises:
            ValueError: If task_name or task_description is empty.
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
        Removes the task with the specified ID.
        
        Args:
            task_id (int): The ID of the task to remove.
        
        Returns:
            bool: True if the task was removed; False if the task was not found.
        
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Searches for tasks where the task_term appears in the name or description (case-insensitive).
        
        Args:
            task_term (str): The term to search for.
        
        Returns:
            list[dict]: A list of matching tasks (each task is a dictionary).
        
        Raises:
            ValueError: If the search term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = task_term.lower()
        results = [
            task for task in self._tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks the specified task as finished.
        
        Args:
            task_id (int): The ID of the task to mark as completed.
        
        Returns:
            bool: True if the task was found and marked finished; False otherwise.
        
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            self._tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all tasks.
        
        Returns:
            list[dict]: A list containing all tasks with their details.
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks.
        
        Returns:
            bool: True once all tasks have been cleared.
        """
        self._tasks.clear()
        return True


def display_tasks(tasks: list):
    """
    Helper function to display tasks in a user-friendly format.
    
    Args:
        tasks (list[dict]): List of task dictionaries to display.
    """
    if not tasks:
        print("No tasks found.")
    else:
        print("\nCurrent Tasks:")
        for task in tasks:
            status = "Finished" if task["is_finished"] else "Pending"
            print(f"ID: {task['id']} | Name: {task['task_name']} | "
                  f"Description: {task['task_description']} | Status: {status}")
        print()


def main():
    """
    Entry point for the console-based todo list application.
    Provides an interactive menu for the user to perform various task operations.
    """
    task_manager = TaskManager()
    menu = """
----------------------------------
Todo List Application Menu:
1. add        - Add a new task
2. remove     - Remove an existing task by ID
3. search     - Search tasks by term
4. finish     - Mark a task as completed
5. get_all    - Display all tasks
6. clear_all  - Delete all tasks
7. exit       - Exit the application
----------------------------------
"""

    print("Welcome to the Todo List Application!")
    
    while True:
        print(menu)
        choice = input("Enter your choice: ").strip().lower()

        if choice in ("1", "add"):
            try:
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}\n")
            except ValueError as e:
                print(f"Error: {e}\n")

        elif choice in ("2", "remove"):
            try:
                id_input = input("Enter the task ID to remove: ").strip()
                if not id_input.isdigit():
                    print("Invalid input. Please enter a positive integer for the task ID.\n")
                    continue
                task_id = int(id_input)
                if task_manager.remove(task_id):
                    print("Task removed successfully.\n")
                else:
                    print("No task found with that ID.\n")
            except ValueError as e:
                print(f"Error: {e}\n")

        elif choice in ("3", "search"):
            try:
                term = input("Enter a search term: ").strip()
                matched_tasks = task_manager.search(term)
                if matched_tasks:
                    print("Search results:")
                    display_tasks(matched_tasks)
                else:
                    print("No matching tasks found.\n")
            except ValueError as e:
                print(f"Error: {e}\n")

        elif choice in ("4", "finish"):
            try:
                id_input = input("Enter the task ID to mark as finished: ").strip()
                if not id_input.isdigit():
                    print("Invalid input. Please enter a positive integer for the task ID.\n")
                    continue
                task_id = int(id_input)
                if task_manager.finish(task_id):
                    print("Task marked as finished.\n")
                else:
                    print("No task found with that ID.\n")
            except ValueError as e:
                print(f"Error: {e}\n")

        elif choice in ("5", "get_all"):
            all_tasks = task_manager.get_all()
            display_tasks(all_tasks)

        elif choice in ("6", "clear_all"):
            confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirm == "yes":
                task_manager.clear_all()
                print("All tasks have been cleared.\n")
            else:
                print("Operation cancelled.\n")

        elif choice in ("7", "exit"):
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option from the menu.\n")


if __name__ == "__main__":
    main()
