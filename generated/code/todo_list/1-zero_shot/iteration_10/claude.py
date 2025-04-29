"""
Todo List Application

A console-based task management system implementing functionality for adding,
removing, searching, and managing tasks, following ISO/IEC 25010 quality standards.
"""
import time
from typing import List, Dict, Union, Optional, Any
import re


class TaskManager:
    """
    Manages a collection of tasks with operations for adding, removing,
    searching, and completing tasks.
    
    Attributes:
        tasks (dict): Dictionary storing tasks with task_id as keys
        next_id (int): Counter for generating unique task IDs
    """
    
    def __init__(self):
        """Initialize the TaskManager with an empty task collection."""
        self.tasks: Dict[int, Dict[str, Any]] = {}
        self.next_id: int = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: The name of the task (non-empty string)
            task_description: The description of the task
            
        Returns:
            int: The unique ID assigned to the new task
            
        Raises:
            ValueError: If task_name is empty or not a string
            TypeError: If inputs are not of the correct type
        """
        # Validate inputs
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        # Create new task
        task_id = self.next_id
        self.tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False,
            'created_at': time.time()
        }
        
        # Increment ID counter
        self.next_id += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: The unique identifier of the task to remove
            
        Returns:
            bool: True if the task was successfully removed, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        # Validate input
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Remove task if it exists
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> List[Dict[str, Any]]:
        """
        Search for tasks containing the specified term in name or description.
        
        Args:
            task_term: The search term to look for in task names and descriptions
            
        Returns:
            list: A list of dictionaries containing tasks that match the search term
            
        Raises:
            TypeError: If task_term is not a string
        """
        # Validate input
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        
        results = []
        
        # If search term is empty, return an empty list
        if not task_term.strip():
            return results
        
        # Case-insensitive search
        pattern = re.compile(re.escape(task_term.strip()), re.IGNORECASE)
        
        for task in self.tasks.values():
            if (pattern.search(task['task_name']) or 
                pattern.search(task['task_description'])):
                results.append(self._format_task_output(task))
        
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The unique identifier of the task to mark as completed
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        # Validate input
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Mark task as finished if it exists
        if task_id in self.tasks:
            # Only update if not already finished
            if not self.tasks[task_id]['is_finished']:
                self.tasks[task_id]['is_finished'] = True
                self.tasks[task_id]['completed_at'] = time.time()
            return True
        
        return False
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks stored in the task manager.
        
        Returns:
            list: A list of dictionaries containing all tasks with their details
        """
        return [self._format_task_output(task) for task in self.tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.
        
        Returns:
            bool: True if the operation was successful
        """
        self.tasks.clear()
        # We don't reset next_id to ensure IDs remain unique across sessions
        return True
    
    def _format_task_output(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a task dictionary for output, ensuring consistent format.
        
        Args:
            task: The task dictionary to format
            
        Returns:
            dict: A formatted task dictionary with standardized fields
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }


def display_menu():
    """Display the main menu options for the todo list application."""
    print("\n===== TODO LIST MANAGER =====")
    print("1. Add a new task")
    print("2. Remove a task")
    print("3. Search tasks")
    print("4. Mark a task as completed")
    print("5. View all tasks")
    print("6. Clear all tasks")
    print("7. Exit")
    print("=============================")


def main():
    """
    Main function to run the todo list application with a command-line interface.
    """
    task_manager = TaskManager()
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-7): ")
            
            if choice == '1':
                task_name = input("Enter task name: ")
                task_description = input("Enter task description: ")
                
                try:
                    task_id = task_manager.add(task_name, task_description)
                    print(f"Task added successfully with ID: {task_id}")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif choice == '2':
                try:
                    task_id = int(input("Enter task ID to remove: "))
                    if task_manager.remove(task_id):
                        print("Task removed successfully")
                    else:
                        print("Task not found")
                except ValueError:
                    print("Error: Please enter a valid integer for the task ID")
                except Exception as e:
                    print(f"Error: {e}")
            
            elif choice == '3':
                search_term = input("Enter search term: ")
                try:
                    results = task_manager.search(search_term)
                    if results:
                        print(f"\nFound {len(results)} matching tasks:")
                        for task in results:
                            status = "COMPLETED" if task['is_finished'] else "PENDING"
                            print(f"ID: {task['id']} - {task['task_name']} [{status}]")
                            print(f"Description: {task['task_description']}\n")
                    else:
                        print("No tasks found matching your search")
                except Exception as e:
                    print(f"Error: {e}")
            
            elif choice == '4':
                try:
                    task_id = int(input("Enter task ID to mark as completed: "))
                    if task_manager.finish(task_id):
                        print("Task marked as completed")
                    else:
                        print("Task not found")
                except ValueError:
                    print("Error: Please enter a valid integer for the task ID")
                except Exception as e:
                    print(f"Error: {e}")
            
            elif choice == '5':
                tasks = task_manager.get_all()
                if tasks:
                    print("\nAll Tasks:")
                    for task in tasks:
                        status = "COMPLETED" if task['is_finished'] else "PENDING"
                        print(f"ID: {task['id']} - {task['task_name']} [{status}]")
                        print(f"Description: {task['task_description']}\n")
                else:
                    print("No tasks available")
            
            elif choice == '6':
                confirm = input("Are you sure you want to clear all tasks? (y/n): ")
                if confirm.lower() == 'y':
                    task_manager.clear_all()
                    print("All tasks have been cleared")
                else:
                    print("Operation cancelled")
            
            elif choice == '7':
                print("Thank you for using the Todo List Manager. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
                
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
