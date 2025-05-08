from typing import Dict, List, Optional, Tuple
import re


class TaskManager:
    """
    A class to manage a to-do list with functions to add, remove, search,
    and manipulate tasks.
    
    Attributes:
        tasks (Dict[int, Dict]): Dictionary storing tasks with task ID as key
        next_id (int): Counter for generating unique task IDs
    """
    
    def __init__(self):
        """Initialize an empty task manager with a task dictionary and ID counter."""
        self.tasks: Dict[int, Dict] = {}
        self.next_id: int = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): Name of the task
            task_description (str): Description of the task
            
        Returns:
            int: The unique ID of the newly created task
            
        Raises:
            ValueError: If task_name or task_description is empty
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty")
        
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
        Remove a task by its ID.
        
        Args:
            task_id (int): ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is negative
            KeyError: If no task with the given ID exists
        """
        if task_id < 1:
            raise ValueError("Task ID must be a positive integer")
            
        if task_id not in self.tasks:
            raise KeyError(f"No task found with ID {task_id}")
            
        del self.tasks[task_id]
        return True
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term (str): Search term to look for in task names and descriptions
            
        Returns:
            List[Dict]: List of tasks matching the search term
            
        Raises:
            ValueError: If task_term is empty
        """
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty")
            
        task_term = task_term.lower().strip()
        result = []
        
        for task in self.tasks.values():
            if (task_term in task["task_name"].lower() or 
                task_term in task["task_description"].lower()):
                result.append(task.copy())
                
        return result
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of the task to mark as completed
            
        Returns:
            bool: True if task was successfully marked as completed
            
        Raises:
            ValueError: If task_id is negative
            KeyError: If no task with the given ID exists
        """
        if task_id < 1:
            raise ValueError("Task ID must be a positive integer")
            
        if task_id not in self.tasks:
            raise KeyError(f"No task found with ID {task_id}")
            
        self.tasks[task_id]["is_finished"] = True
        return True
    
    def get_all(self) -> List[Dict]:
        """
        Get all tasks.
        
        Returns:
            List[Dict]: List of all tasks with their details
        """
        return [task.copy() for task in self.tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Clear all tasks.
        
        Returns:
            bool: True if all tasks were successfully cleared
        """
        self.tasks.clear()
        return True
