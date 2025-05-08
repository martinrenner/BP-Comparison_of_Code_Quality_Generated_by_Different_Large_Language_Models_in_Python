from typing import Dict, List, Optional, Union
import re
from datetime import datetime


class TaskManager:
    """
    A class for managing a to-do list with tasks.

    This class implements operations for adding, removing, searching, and managing tasks
    in a to-do list application. It provides an efficient, in-memory storage solution
    with comprehensive error handling.
    """

    def __init__(self):
        """Initialize an empty task manager with an in-memory data structure."""
        self._tasks: Dict[int, Dict] = {}  # Dictionary for O(1) lookups by ID
        self._next_id: int = 1  # Counter for assigning unique IDs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the to-do list.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID of the newly added task.

        Raises:
            ValueError: If the task name or description is empty.
        """
        # Validate inputs
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty")

        # Clean inputs
        task_name = task_name.strip()
        task_description = task_description.strip()
        
        # Create a new task with a unique ID
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name,
            'task_description': task_description,
            'is_finished': False,
            'created_at': datetime.now(),
        }
        
        # Increment the ID counter for the next task
        self._next_id += 1
        
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.

        Raises:
            ValueError: If the task ID is invalid (negative or zero).
        """
        # Validate task ID
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        # Check if task exists
        if task_id not in self._tasks:
            return False
            
        # Remove the task
        del self._tasks[task_id]
        return True

    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.

        Args:
            task_term (str): The search term to look for in task names and descriptions.

        Returns:
            list[dict]: A list of tasks matching the search term.

        Raises:
            ValueError: If the search term is empty.
        """
        # Validate search term
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty")
            
        task_term = task_term.lower().strip()
        
        # Find matching tasks (case-insensitive)
        results = []
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                results.append(self._format_task_output(task))
                
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.

        Args:
            task_id (int): The unique ID of the task to mark as completed.

        Returns:
            bool: True if the task was successfully marked as completed, False if the task doesn't exist.

        Raises:
            ValueError: If the task ID is invalid (negative or zero).
        """
        # Validate task ID
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        # Check if task exists
        if task_id not in self._tasks:
            return False
            
        # Mark task as finished
        self._tasks[task_id]['is_finished'] = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.

        Returns:
            list[dict]: A list of all tasks with their details.
        """
        return [self._format_task_output(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Delete all tasks.

        Returns:
            bool: True if all tasks were successfully deleted.
        """
        self._tasks.clear()
        return True
        
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format a task for output according to the required format.
        
        Args:
            task (Dict): The internal task representation.
            
        Returns:
            Dict: The formatted task with only the required fields.
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }


def display_menu() -> None:
    """Display the application menu options."""
    print("\n===== Todo List Application =====")
    print("1. Add a new task")
    print("2. Remove a task")
    print("3. Search tasks")
    print("4. Mark a task as completed")
    print("5. View all tasks")
    print("6. Clear all tasks")
    print("0. Exit")
    print("================================")


def display_tasks(tasks: List[Dict]) -> None:
    """
    Display a list of tasks in a formatted way.
    
    Args:
        tasks (List[Dict]): List of tasks to display.
    """
    if not tasks:
        print("No tasks found.")
        return
        
    print("\n--- Tasks ---")
    for task in tasks:
        status = "✓ Completed" if task['is_finished'] else "◯ Pending"
        print(f"ID: {task['id']} [{status}]")
        print(f"Name: {task['task_name']}")
        print(f"Description: {task['task_description']}")
        print("-------------------")


def run_application() -> None:
    """Run the Todo List Application with an interactive console interface."""
    task_manager = TaskManager()
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (0-6): ")
            
            if choice == '0':
                print("Exiting application. Goodbye!")
                break
                
            elif choice == '1':
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                
                try:
                    task_id = task_manager.add(name, description)
                    print(f"Task added successfully with ID: {task_id}")
                except ValueError as e:
                    print(f"Error: {str(e)}")
                    
            elif choice == '2':
                try:
                    task_id = int(input("Enter task ID to remove: "))
                    if task_manager.remove(task_id):
                        print(f"Task {task_id} successfully removed.")
                    else:
                        print(f"Task with ID {task_id} not found.")
                except ValueError as e:
                    print(f"Error: {str(e) if 'Task ID' in str(e) else 'Invalid ID format. Please enter a number.'}")
                    
            elif choice == '3':
                try:
                    search_term = input("Enter search term: ")
                    results = task_manager.search(search_term)
                    display_tasks(results)
                except ValueError as e:
                    print(f"Error: {str(e)}")
                    
            elif choice == '4':
                try:
                    task_id = int(input("Enter task ID to mark as completed: "))
                    if task_manager.finish(task_id):
                        print(f"Task {task_id} marked as completed.")
                    else:
                        print(f"Task with ID {task_id} not found.")
                except ValueError as e:
                    print(f"Error: {str(e) if 'Task ID' in str(e) else 'Invalid ID format. Please enter a number.'}")
                    
            elif choice == '5':
                tasks = task_manager.get_all()
                display_tasks(tasks)
                
            elif choice == '6':
                confirm = input("Are you sure you want to clear all tasks? (y/n): ")
                if confirm.lower() == 'y':
                    task_manager.clear_all()
                    print("All tasks cleared successfully.")
                else:
                    print("Operation canceled.")
                    
            else:
                print("Invalid choice. Please try again.")
                
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    run_application()
