"""
Console-Based Todo List App

This module implements a console-based todo list app using OOP and adheres
to the ISO/IEC 25010 software quality standards regarding functionality,
performance, modularity, security, testability, and readability.

The TaskManager class provides methods to add, remove, search, finish, get all,
and clear tasks. Each task is stored in-memory as a dictionary with the keys:
    - id: Unique identifier for the task.
    - task_name: Name of the task.
    - task_description: Detailed description of the task.
    - is_finished: Boolean flag indicating whether the task is completed.

The app includes simple command-line interaction with robust validation and 
error handling to ensure proper usage.
"""

class TaskManager:
    """
    Manages a collection of tasks in an in-memory dictionary.
    
    Each task is represented as a dictionary with:
        - id (int): Unique task identifier.
        - task_name (str): Name of the task.
        - task_description (str): Description of the task.
        - is_finished (bool): Completion status of the task.
    """
    
    def __init__(self):
        # Dictionary to store tasks by their unique ID for efficient lookup, insertion, and deletion.
        self._tasks = {}  # key: task_id, value: task dict
        self._next_id = 1  # Auto-incremented task ID
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task with the specified name and description.

        Parameters:
            task_name (str): The name of the task. Must be non-empty.
            task_description (str): The description of the task. Must be non-empty.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If either task_name or task_description is empty or only whitespace.
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty.")
        
        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self._next_id += 1
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its unique ID.

        Parameters:
            task_id (int): The unique identifier of the task to remove. Must be a positive integer.

        Returns:
            bool: True if the task was successfully removed; False if no task with that ID exists.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        else:
            return False
    
    def search(self, task_term: str) -> list:
        """
        Search for tasks whose name or description includes the given search term.

        Parameters:
            task_term (str): The term to search for in task names and descriptions.
                             Must be a non-empty string.

        Returns:
            list[dict]: A list of task dictionaries that match the search criteria.
                        Each dictionary includes 'id', 'task_name', 'task_description', and 'is_finished'.

        Raises:
            ValueError: If task_term is empty or contains only whitespace.
        """
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty.")
        term_lower = task_term.strip().lower()
        result = []
        for task in self._tasks.values():
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower():
                result.append(task)
        return result
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a specific task as finished.

        Parameters:
            task_id (int): The ID of the task to mark as completed. Must be a positive integer.

        Returns:
            bool: True if the task was successfully marked as finished; False if the task does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id in self._tasks:
            self._tasks[task_id]["is_finished"] = True
            return True
        else:
            return False
    
    def get_all(self) -> list:
        """
        Retrieve all tasks.

        Returns:
            list[dict]: A list of all task dictionaries with their details.
                        Each includes 'id', 'task_name', 'task_description', and 'is_finished'.
        """
        return list(self._tasks.values())
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the task manager.

        Returns:
            bool: True indicating that all tasks were successfully cleared.
        """
        self._tasks.clear()
        return True

def display_menu() -> None:
    """
    Display the main menu options for the Todo List App.
    """
    print("\nTodo List App - Options:")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Search Tasks")
    print("4. Finish Task")
    print("5. Get All Tasks")
    print("6. Clear All Tasks")
    print("7. Exit")

def main() -> None:
    """
    Main function to run the console-based todo list application.
    
    Handles user input, calls methods from TaskManager,
    and displays results or error messages where appropriate.
    """
    manager = TaskManager()
    print("Welcome to the Console Todo List App!")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            # Add Task
            task_name = input("Enter task name: ").strip()
            task_description = input("Enter task description: ").strip()
            try:
                task_id = manager.add(task_name, task_description)
                print(f"Task added with ID: {task_id}")
            except ValueError as ve:
                print(f"Error adding task: {ve}")
                
        elif choice == "2":
            # Remove Task
            id_str = input("Enter task ID to remove: ").strip()
            try:
                task_id = int(id_str)
                if manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")
            except ValueError as ve:
                print(f"Invalid input: {ve}")
                
        elif choice == "3":
            # Search Tasks
            search_term = input("Enter search term: ").strip()
            try:
                results = manager.search(search_term)
                if results:
                    print("Search results:")
                    for task in results:
                        print(f"ID: {task['id']}, Name: {task['task_name']}, "
                              f"Description: {task['task_description']}, Finished: {task['is_finished']}")
                else:
                    print("No matching tasks found.")
            except ValueError as ve:
                print(f"Invalid input: {ve}")
                
        elif choice == "4":
            # Finish Task
            id_str = input("Enter task ID to mark as finished: ").strip()
            try:
                task_id = int(id_str)
                if manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")
            except ValueError as ve:
                print(f"Invalid input: {ve}")
                
        elif choice == "5":
            # Get All Tasks
            tasks = manager.get_all()
            if tasks:
                print("All tasks:")
                for task in tasks:
                    print(f"ID: {task['id']}, Name: {task['task_name']}, "
                          f"Description: {task['task_description']}, Finished: {task['is_finished']}")
            else:
                print("No tasks available.")
                
        elif choice == "6":
            # Clear All Tasks
            confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirm == "yes":
                manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Clear all canceled.")
                
        elif choice == "7":
            # Exit
            print("Exiting Todo List App. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == '__main__':
    main()
