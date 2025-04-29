"""
Console-based Todo List App that meets ISO/IEC 25010 quality requirements.
This application uses an object-oriented design to manage tasks with operations to add, remove,
search, mark as finished, list, and clear all tasks. Tasks are stored in an in-memory data structure.
Each task is represented as a dictionary with the following format:
    { "id": int, "task_name": str, "task_description": str, "is_finished": bool }
"""

class TaskManager:
    """
    A class to manage tasks in a todo list application.
    
    Methods:
        add(task_name: str, task_description: str) -> int
        remove(task_id: int) -> bool
        search(task_term: str) -> list[dict]
        finish(task_id: int) -> bool
        get_all() -> list[dict]
        clear_all() -> bool
    """
    def __init__(self):
        """
        Initializes the TaskManager with an empty task storage and a task ID counter.
        """
        self.tasks = {}  # In-memory storage for tasks keyed by their unique ID.
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task with the provided name and description.
        
        Args:
            task_name (str): The name of the task; must be a non-empty string.
            task_description (str): The description of the task; must be non-empty.
        
        Returns:
            int: The unique ID assigned to the new task.
        
        Raises:
            ValueError: If the task name or description is empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str) or not task_description.strip():
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
        Removes a task identified by the given task ID.
        
        Args:
            task_id (int): The unique ID of the task to be removed; must be positive.
        
        Returns:
            bool: True if the task was successfully removed; False if the task does not exist.
        
        Raises:
            ValueError: If the task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            return False

        del self.tasks[task_id]
        return True

    def search(self, task_term: str) -> list:
        """
        Searches for tasks that contain the given term in either their name or description.
        The search is case-insensitive.
        
        Args:
            task_term (str): A non-empty search string.
        
        Returns:
            list[dict]: A list of tasks that match the search term. Each task is a dictionary 
                        in the format: { "id", "task_name", "task_description", "is_finished" }.
        
        Raises:
            ValueError: If the search term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term cannot be empty.")
        term = task_term.lower()

        matching_tasks = []
        for task in self.tasks.values():
            if term in task["task_name"].lower() or term in task["task_description"].lower():
                matching_tasks.append(task)
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks the task with the given task ID as finished.
        
        Args:
            task_id (int): The unique ID of the task to mark as finished.
        
        Returns:
            bool: True if the task was successfully marked as finished; False if the task does not exist.
        
        Raises:
            ValueError: If the task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            return False

        self.tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> list:
        """
        Retrieves a list of all tasks.
        
        Returns:
            list[dict]: A list of all tasks, where each task is represented as a dictionary containing
                        id, task_name, task_description, and is_finished.
        """
        # Returning tasks sorted by their ID for consistent ordering.
        return [self.tasks[tid] for tid in sorted(self.tasks)]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the manager.
        
        Returns:
            bool: True after all tasks have been cleared.
        """
        self.tasks.clear()
        return True


def display_task(task: dict) -> None:
    """
    Helper function to print a task's details in a formatted way.
    
    Args:
        task (dict): A task dictionary with keys 'id', 'task_name', 'task_description', 'is_finished'.
    """
    status = "Completed" if task["is_finished"] else "Pending"
    print(f"ID: {task['id']} | Name: {task['task_name']} | Description: {task['task_description']} | Status: {status}")


def print_menu() -> None:
    """
    Displays the main menu options for the console-based todo list app.
    """
    print("\n----- Todo List Menu -----")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Search Tasks")
    print("4. Mark Task as Finished")
    print("5. List All Tasks")
    print("6. Clear All Tasks")
    print("7. Exit")


def main():
    """
    The main function orchestrates the console-based user interaction and operations on the TaskManager.
    """
    manager = TaskManager()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        try:
            if choice == "1":
                # Add Task
                name = input("Enter task name: ").strip()
                desc = input("Enter task description: ").strip()
                task_id = manager.add(name, desc)
                print(f"Task added successfully with ID: {task_id}")
            
            elif choice == "2":
                # Remove Task
                try:
                    task_id = int(input("Enter task ID to remove: ").strip())
                    if manager.remove(task_id):
                        print("Task removed successfully.")
                    else:
                        print("Task not found.")
                except ValueError as ve:
                    print("Invalid input. Please enter a valid positive integer for task ID.")
            
            elif choice == "3":
                # Search Tasks
                term = input("Enter search term: ").strip()
                results = manager.search(term)
                if results:
                    print(f"Found {len(results)} matching task(s):")
                    for task in results:
                        display_task(task)
                else:
                    print("No tasks found matching the search term.")
            
            elif choice == "4":
                # Mark Task as Finished
                try:
                    task_id = int(input("Enter task ID to mark as finished: ").strip())
                    if manager.finish(task_id):
                        print("Task marked as finished.")
                    else:
                        print("Task not found.")
                except ValueError as ve:
                    print("Invalid input. Please enter a valid positive integer for task ID.")
            
            elif choice == "5":
                # List All Tasks
                tasks = manager.get_all()
                if tasks:
                    print("Listing all tasks:")
                    for task in tasks:
                        display_task(task)
                else:
                    print("No tasks available.")
            
            elif choice == "6":
                # Clear All Tasks
                confirmation = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirmation == "yes":
                    manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear all tasks operation cancelled.")
            
            elif choice == "7":
                # Exit the application
                print("Exiting the Todo List App. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please select a valid option from the menu.")
        
        except ValueError as error:
            # Catch any validation errors raised during task operations.
            print(f"Error: {error}")

if __name__ == "__main__":
    main()
