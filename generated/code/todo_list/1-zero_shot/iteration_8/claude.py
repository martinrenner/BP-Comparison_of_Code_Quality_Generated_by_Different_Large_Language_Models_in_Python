"""
Todo List Application

A console-based todo list manager that implements the functionality required
by ISO/IEC 25010 standards for software quality.
"""
from typing import List, Dict, Optional, Any, Union
import re
from datetime import datetime


class TaskManager:
    """
    Manages tasks in a todo list with operations for adding, removing,
    searching, completing tasks and more.
    
    Attributes:
        _tasks (dict): In-memory storage of tasks
        _next_id (int): Auto-incrementing counter for task IDs
    """
    
    def __init__(self):
        """Initialize an empty task manager with a counter for task IDs."""
        self._tasks = {}  # Using a dictionary for O(1) lookups by ID
        self._next_id = 1  # Start IDs at 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name: The name/title of the task
            task_description: A detailed description of the task
            
        Returns:
            int: The unique ID of the newly created task
            
        Raises:
            ValueError: If task_name or task_description is empty
        """
        # Input validation
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty")
            
        # Create task with sanitized inputs
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        self._next_id += 1
        
        return task_id
        
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id: The unique identifier of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is negative or not an integer
        """
        # Input validation
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        # Check if task exists before attempting removal
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
        
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term: The search term to look for in task names and descriptions
            
        Returns:
            List[Dict]: A list of tasks matching the search criteria
            
        Raises:
            ValueError: If task_term is empty
        """
        # Input validation
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty")
            
        task_term = task_term.strip().lower()
        result = []
        
        # Search in both task name and description
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                result.append(self._format_task_output(task))
                
        return result
        
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The unique identifier of the task to mark as completed
            
        Returns:
            bool: True if task was successfully marked as completed, False otherwise
            
        Raises:
            ValueError: If task_id is negative or not an integer
        """
        # Input validation
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        # Update task if it exists
        if task_id in self._tasks:
            # Only update if not already finished
            if not self._tasks[task_id]['is_finished']:
                self._tasks[task_id]['is_finished'] = True
                self._tasks[task_id]['updated_at'] = datetime.now()
            return True
        return False
        
    def get_all(self) -> List[Dict]:
        """
        Get all tasks in the todo list.
        
        Returns:
            List[Dict]: A list of all tasks with their details
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
        
    def clear_all(self) -> bool:
        """
        Remove all tasks from the todo list.
        
        Returns:
            bool: True if all tasks were successfully cleared
        """
        self._tasks.clear()
        return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format a task for output according to the required format.
        
        Args:
            task: The task dictionary with all task data
            
        Returns:
            Dict: A dictionary with the required task fields
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }


def main():
    """
    Main function to demonstrate the TaskManager functionality.
    """
    task_manager = TaskManager()
    
    # Example usage
    try:
        print("Adding tasks...")
        task1_id = task_manager.add("Complete project", "Finish the Python todo list project")
        task2_id = task_manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
        task3_id = task_manager.add("Call mom", "Don't forget mom's birthday")
        
        print("\nAll tasks:")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            print(f"ID: {task['id']}, Name: {task['task_name']}, " 
                  f"Finished: {task['is_finished']}")
        
        print("\nMarking task as completed...")
        task_manager.finish(task1_id)
        
        print("\nSearching for 'birthday'...")
        birthday_tasks = task_manager.search("birthday")
        for task in birthday_tasks:
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Description: {task['task_description']}")
        
        print("\nRemoving task...")
        task_manager.remove(task2_id)
        
        print("\nRemaining tasks:")
        remaining_tasks = task_manager.get_all()
        for task in remaining_tasks:
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Finished: {task['is_finished']}")
        
        print("\nClearing all tasks...")
        task_manager.clear_all()
        print(f"Tasks after clearing: {len(task_manager.get_all())}")
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
