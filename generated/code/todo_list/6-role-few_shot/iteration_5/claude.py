from typing import List, Dict, Optional, Union
from datetime import datetime
import re


class TaskManager:
    """
    A class responsible for managing tasks in a to-do list application.
    
    This class provides functionalities to add, remove, search, complete tasks,
    retrieve all tasks, and clear the task list.
    """
    
    def __init__(self):
        """Initialize the TaskManager with an empty task dictionary and a task ID counter."""
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.
            
        Returns:
            int: The unique ID assigned to the new task.
            
        Raises:
            ValueError: If task_name or task_description is empty or not a string.
        """
        # Input validation
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")
            
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False,
            'created_at': datetime.now()
        }
        self._next_id += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): The ID of the task to be removed.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
            
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term (str): The search term to look for in task name or description.
            
        Returns:
            List[Dict]: A list of tasks matching the search term.
            
        Raises:
            ValueError: If task_term is empty or not a string.
        """
        if not isinstance(task_term, str):
            raise ValueError("Search term must be a string.")
        
        task_term = task_term.strip().lower()
        if not task_term:
            return []
            
        result = []
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                result.append(self._format_task_output(task))
        
        return result
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed by its ID.
        
        Args:
            task_id (int): The ID of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
            
        if task_id in self._tasks:
            # Only update if not already finished
            if not self._tasks[task_id]['is_finished']:
                self._tasks[task_id]['is_finished'] = True
                self._tasks[task_id]['completed_at'] = datetime.now()
            return True
        return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        
        Returns:
            List[Dict]: A list of all tasks with their details.
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Delete all tasks.
        
        Returns:
            bool: Always returns True as the operation always succeeds.
        """
        self._tasks.clear()
        return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format a task for output according to the specified format.
        
        Args:
            task (Dict): The task to format.
            
        Returns:
            Dict: A dictionary with the formatted task information.
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }


# Example usage
if __name__ == "__main__":
    # This block demonstrates how to use the TaskManager class
    task_manager = TaskManager()
    
    # Add some tasks
    task_id1 = task_manager.add("Complete project", "Finish the Python project by Friday")
    task_id2 = task_manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
    
    # Mark a task as completed
    task_manager.finish(task_id1)
    
    # Search for tasks
    results = task_manager.search("project")
    for task in results:
        print(f"Found task: {task['task_name']}")
    
    # Get all tasks
    all_tasks = task_manager.get_all()
    print(f"Total tasks: {len(all_tasks)}")
    
    # Remove a task
    task_manager.remove(task_id2)
    
    # Verify task was removed
    all_tasks = task_manager.get_all()
    print(f"Tasks after removal: {len(all_tasks)}")
    
    # Clear all tasks
    task_manager.clear_all()
    print(f"Tasks after clearing: {len(task_manager.get_all())}")
