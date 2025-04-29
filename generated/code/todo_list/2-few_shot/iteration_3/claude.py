from typing import List, Dict, Optional, Union
import re

class TaskManager:
    """
    A task management system that allows users to create, manage, and track tasks.
    
    This class provides functionality to add, remove, search for, complete, and
    retrieve tasks, addressing the requirements of ISO/IEC 25010 for functionality,
    reliability, usability, and maintainability.
    """
    
    def __init__(self):
        """Initialize an empty task manager with a dictionary to store tasks and a counter for task IDs."""
        self._tasks: Dict[int, Dict] = {}
        self._id_counter: int = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): A detailed description of the task.
            
        Returns:
            int: The unique ID assigned to the new task.
            
        Raises:
            ValueError: If the task name or description is empty.
        """
        # Validate inputs
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name must be a non-empty string")
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description must be a non-empty string")
            
        # Create and store the new task
        task_id = self._id_counter
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name,
            'task_description': task_description,
            'is_finished': False
        }
        
        # Increment the ID counter for the next task
        self._id_counter += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its unique ID.
        
        Args:
            task_id (int): The unique identifier of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If the task ID is invalid.
        """
        # Validate the task ID
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        # Remove the task if it exists
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description containing the search term.
        
        Args:
            task_term (str): The term to search for in task names and descriptions.
            
        Returns:
            list[dict]: A list of tasks matching the search criteria.
            
        Raises:
            ValueError: If the search term is empty.
        """
        # Validate the search term
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term must be a non-empty string")
            
        # Create a case-insensitive pattern for searching
        pattern = re.compile(re.escape(task_term), re.IGNORECASE)
        
        # Find and return matching tasks
        results = []
        for task in self._tasks.values():
            if (pattern.search(task['task_name']) or 
                pattern.search(task['task_description'])):
                results.append(task.copy())
                
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique identifier of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If the task ID is invalid.
        """
        # Validate the task ID
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        # Mark the task as finished if it exists
        if task_id in self._tasks:
            # If the task is already finished, return False to indicate no change
            if self._tasks[task_id]['is_finished']:
                return False
            
            self._tasks[task_id]['is_finished'] = True
            return True
        
        return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks currently stored in the task manager.
        
        Returns:
            list[dict]: A list of all tasks with their details.
        """
        # Return a deep copy of all tasks to prevent modification of internal data
        return [task.copy() for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.
        
        Returns:
            bool: True if tasks were cleared successfully, False if there were no tasks to clear.
        """
        if not self._tasks:
            return False
            
        self._tasks.clear()
        return True
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """
        Retrieve a specific task by its ID.
        
        Args:
            task_id (int): The unique identifier of the task to retrieve.
            
        Returns:
            Optional[Dict]: The task dictionary if found, None otherwise.
            
        Raises:
            ValueError: If the task ID is invalid.
        """
        # Validate the task ID
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        # Return a copy of the task if it exists
        if task_id in self._tasks:
            return self._tasks[task_id].copy()
            
        return None


def display_menu():
    """Display the available commands for the todo list application."""
    print("\n===== TODO LIST APPLICATION =====")
    print("1. Add a new task")
    print("2. Remove a task")
    print("3. Search for tasks")
    print("4. Mark a task as finished")
    print("5. Show all tasks")
    print("6. Clear all tasks")
    print("7. Exit")
    print("=================================")


def display_tasks(tasks: List[Dict]):
    """
    Display a list of tasks in a formatted manner.
    
    Args:
        tasks (List[Dict]): The list of tasks to display.
    """
    if not tasks:
        print("No tasks found.")
        return
        
    print("\n----- Tasks -----")
    for task in tasks:
        status = "[COMPLETED]" if task['is_finished'] else "[PENDING]"
        print(f"ID: {task['id']} {status}")
        print(f"Name: {task['task_name']}")
        print(f"Description: {task['task_description']}")
        print("-----------------")


def main():
    """Main function to run the todo list application."""
    task_manager = TaskManager()
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-7): ")
            
            if choice == '1':
                # Add a new task
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")
                
            elif choice == '2':
                # Remove a task
                task_id = int(input("Enter task ID to remove: "))
                if task_manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")
                    
            elif choice == '3':
                # Search for tasks
                term = input("Enter search term: ")
                matching_tasks = task_manager.search(term)
                display_tasks(matching_tasks)
                
            elif choice == '4':
                # Mark a task as finished
                task_id = int(input("Enter task ID to mark as finished: "))
                if task_manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found or already finished.")
                    
            elif choice == '5':
                # Show all tasks
                all_tasks = task_manager.get_all()
                display_tasks(all_tasks)
                
            elif choice == '6':
                # Clear all tasks
                confirm = input("Are you sure you want to clear all tasks? (yes/no): ").lower()
                if confirm == 'yes' and task_manager.clear_all():
                    print("All tasks have been cleared.")
                else:
                    print("No tasks were cleared.")
                    
            elif choice == '7':
                # Exit the application
                print("Thank you for using the Todo List Application. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
                
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
